// AI 对话配置
// 填入 Google Gemini API Key 即可启用真实 AI（免费申请：https://aistudio.google.com/apikey）
// 留空则使用内置本地助手（可回答网站相关问题）

var CHAT_CONFIG = {
  apiKey: "",
  model: "gemini-2.0-flash",
  botName: "handsome feng 的 AI 助手",
  systemPrompt:
    "你是 handsome feng 个人网站上的 AI 助手。网站主人叫 handsome feng，" +
    "网站分为三个板块：学习（编程、阅读、笔记）、生活（旅行、咖啡、摄影）、" +
    "娱乐（游戏、电影、音乐、运动）。联系方式邮箱是 xfxfyyds@gmail.com。" +
    "请用简洁、友好、自然的中文回答，每次回复控制在 150 字以内。"
};
