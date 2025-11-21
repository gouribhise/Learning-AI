import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: ".env");
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'QuoteGenerator',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const QuoteGenerator(),
    );
  }
}

class QuoteGenerator extends StatefulWidget {
  const QuoteGenerator({super.key});

  @override
  _QuoteGeneratorState createState() => _QuoteGeneratorState();
}

class _QuoteGeneratorState extends State<QuoteGenerator> {
  final TextEditingController controller = TextEditingController();
  bool loading = false;

  late final String apiKey;
  int selectedCount = 3;

  List<String> quotes = [];

  @override
  void initState() {
    super.initState();
    apiKey = dotenv.env['HF_TOKEN'] ?? "";
  }

  List<String> cleanQuotes(String raw, String topic, int expectedCount) {
    final lines =
        raw
            .split('\n')
            .map((q) => q.trim())
            .where((q) => q.isNotEmpty)
            .toList();

    final filtered =
        lines.where((q) {
          final lower = q.toLowerCase();
          return !lower.contains("i cannot") &&
              !lower.contains("i'm sorry") &&
              !lower.contains("as an ai") &&
              !q.startsWith("Sure") &&
              !q.startsWith("Here") &&
              q.length > 8;
        }).toList();

    final matchesTopic =
        filtered.where((q) {
          return q.toLowerCase().contains(topic.toLowerCase());
        }).toList();

    if (matchesTopic.length < expectedCount) {
      return [];
    }

    return matchesTopic;
  }

  Future<void> generateQuote(String topic) async {
    setState(() {
      loading = true;
      quotes = [];
    });

    try {
      const url = "https://router.huggingface.co/v1/chat/completions";

      final headers = {
        "Authorization": "Bearer $apiKey",
        "Content-Type": "application/json",
      };

      final body = jsonEncode({
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [
          {
            "role": "user",
            "content":
                "Create $selectedCount short meaningful quotes on the topic: $topic. "
                "Return ONLY clean plain text quotes, each on a new line, without numbers, bullets, asterisks, emojis, or decorative symbols.",
          },
        ],
        "max_tokens": 150,
      });

      final response = await http
          .post(Uri.parse(url), headers: headers, body: body)
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final raw = data["choices"][0]["message"]["content"] ?? "";

        final cleaned = cleanQuotes(raw, topic, selectedCount);

        if (cleaned.isEmpty) {
          setState(() {
            quotes = [
              "No quotes found for this topic. Please enter a different topic.",
            ];
          });
        } else {
          setState(() {
            quotes = cleaned;
          });
        }
      } else {
        setState(() {
          quotes = ["Server error: ${response.statusCode}. Please try again."];
        });
      }
    } on http.ClientException {
      setState(() {
        quotes = ["Network error. Please check your internet connection."];
      });
    } on TimeoutException {
      setState(() {
        quotes = ["Request timed out. Please try again."];
      });
    } catch (e) {
      setState(() {
        quotes = ["Something went wrong: $e"];
      });
    }

    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("AI Quotes Generator")),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            TextField(
              controller: controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: "Enter Topic",
              ),
            ),

            const SizedBox(height: 20),

            DropdownButton(
              value: selectedCount,
              items:
                  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                      .map(
                        (num) => DropdownMenuItem(
                          value: num,
                          child: Text("$num Quotes"),
                        ),
                      )
                      .toList(),
              onChanged: (value) {
                setState(() => selectedCount = value as int);
              },
            ),

            const SizedBox(height: 20),

            ElevatedButton(
              child: const Text("Generate Quote"),
              onPressed: () {
                final topic = controller.text.trim();
                if (topic.isNotEmpty) generateQuote(topic);
              },
            ),

            const SizedBox(height: 20),

            if (loading) const CircularProgressIndicator(),

            if (!loading && quotes.isNotEmpty)
              Expanded(
                child: ListView.builder(
                  itemCount: quotes.length,
                  itemBuilder: (context, index) {
                    return TweenAnimationBuilder(
                      duration: Duration(milliseconds: 500 + (index * 120)),
                      tween: Tween<Offset>(
                        begin: const Offset(0, 0.3),
                        end: Offset.zero,
                      ),
                      curve: Curves.easeOut,
                      builder: (context, offset, child) {
                        return Transform.translate(
                          offset: Offset(0, offset.dy * 40),
                          child: child,
                        );
                      },
                      child: Card(
                        elevation: 3,
                        margin: const EdgeInsets.symmetric(vertical: 8),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Text(
                            quotes[index],
                            style: const TextStyle(fontSize: 18),
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
    );
  }
}
