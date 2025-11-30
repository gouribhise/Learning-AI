import express from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const API_URL = "https://router.huggingface.co/v1/chat/completions";
const API_KEY = process.env.HF_TOKEN;

 
function cleanQuotes(raw, topic, expectedCount) {
  const lines = raw
    .split("\n")
    .map((q) => q.trim())
    .filter((q) => q.length > 0);

  const filtered = lines.filter((q) => {
    const lower = q.toLowerCase();
    return (
      !lower.includes("i cannot") &&
      !lower.includes("i'm sorry") &&
      !lower.includes("as an ai") &&
      !q.startsWith("Sure") &&
      !q.startsWith("Here") &&
      q.length > 8
    );
  });

  const matchesTopic = filtered.filter((q) =>
    q.toLowerCase().includes(topic.toLowerCase())
  );

  if (matchesTopic.length < expectedCount) {
    return [];
  }
  return matchesTopic;
}

 
app.post("/generate", async (req, res) => {
  const { topic, count } = req.body;

  if (!topic || !count) {
    return res.status(400).json({
      error: "Topic and count are required.",
    });
  }

  try {
    const response = await axios.post(
      API_URL,
      {
        model: "deepseek-ai/DeepSeek-V3-0324",
        messages: [
          {
            role: "user",
            content:
              `Create ${count} short meaningful quotes on the topic: ${topic}. ` +
              `Return ONLY clean plain text quotes, each on a new line, without numbers, bullets, asterisks, emojis, or decorative symbols.`,
          },
        ],
        max_tokens: 150,
      },
      {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
        },
        timeout: 10000, // 10 seconds
      }
    );

    const raw = response.data.choices?.[0]?.message?.content || "";

    const cleaned = cleanQuotes(raw, topic, count);

    if (cleaned.length === 0) {
      return res.json({
        quotes: [
          "No quotes found for this topic. Please enter a different topic.",
        ],
      });
    }

    return res.json({ quotes: cleaned });
  } catch (err) {
    if (err.code === "ECONNABORTED") {
      return res.status(408).json({ error: "Request timed out." });
    }

    if (err.response) {
      return res.status(err.response.status).json({
        error: `Server error: ${err.response.status}`,
      });
    }

    return res.status(500).json({
      error: `Something went wrong: ${err.message}`,
    });
  }
});

app.listen(3000, () => console.log("Server running on port 3000"));