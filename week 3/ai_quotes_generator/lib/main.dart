import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
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
  String result = "";
  bool loading = false;

  late final String apiKey;
  int selectedCount = 3; // default quotes count

  @override
  void initState() {
    super.initState();
    apiKey = dotenv.env['HF_TOKEN'] ?? "";
  }

  Future<void> generateQuote(String topic) async {
    setState(() => loading = true);

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
              "Create $selectedCount meaningful quotes on the topic: $topic",
        },
      ],
      "max_tokens": 150,
    });

    final response = await http.post(
      Uri.parse(url),
      headers: headers,
      body: body,
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      setState(() {
        result = data["choices"][0]["message"]["content"] ?? "No output";
      });
    } else {
      setState(() {
        result = "Error: ${response.body}";
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
                  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) {
                    return DropdownMenuItem(
                      value: num,
                      child: Text("$num Quotes"),
                    );
                  }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedCount = value as int;
                });
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
            if (!loading && result.isNotEmpty)
              Text(
                result,
                style: const TextStyle(fontSize: 18),
                textAlign: TextAlign.center,
              ),
          ],
        ),
      ),
    );
  }
}
