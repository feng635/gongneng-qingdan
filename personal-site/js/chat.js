(function () {
  "use strict";

  var widget = document.getElementById("chatWidget");
  var panel = document.getElementById("chatPanel");
  var toggle = document.getElementById("chatToggle");
  var closeBtn = document.getElementById("chatClose");
  var messagesEl = document.getElementById("chatMessages");
  var input = document.getElementById("chatInput");
  var sendBtn = document.getElementById("chatSend");
  var statusEl = document.getElementById("chatStatus");

  var isOpen = false;
  var isLoading = false;
  var history = [];
  var greeted = false;

  var useAI = !!(typeof CHAT_CONFIG !== "undefined" && CHAT_CONFIG.apiKey);

  if (useAI) {
    statusEl.textContent = "在线 · Gemini AI";
  }

  // ===== 本地助手（无 API Key 时使用） =====
  var localReplies = [
    {
      match: function (t) { return /你好|嗨|hello|hi|在吗/.test(t); },
      reply: "你好！我是 handsome feng 网站上的 AI 助手 👋 你可以问我关于这个网站的问题，比如三个板块是做什么的，或者怎么联系他。"
    },
    {
      match: function (t) { return /学习|study|读书|代码|编程/.test(t); },
      reply: "「学习」板块记录 handsome feng 的学习日常：前端开发、英语阅读、笔记整理等。你可以滚动到页面上方的学习板块看看相关照片 ✦"
    },
    {
      match: function (t) { return /生活|life|旅行|咖啡|摄影/.test(t); },
      reply: "「生活」板块是他的生活剪影：城市漫步、旅行、咖啡探店和摄影。绿色主题的那个区域就是～"
    },
    {
      match: function (t) { return /娱乐|fun|游戏|电影|音乐|运动/.test(t); },
      reply: "「娱乐」板块放的是游戏、电影、音乐和运动相关的内容。忙碌之余，也要留点纯粹的快乐嘛 🎮"
    },
    {
      match: function (t) { return /联系|邮箱|email|gmail|谷歌|google/.test(t); },
      reply: "你可以通过 Gmail 联系他：xfxfyyds@gmail.com\n\n页脚也有邮箱链接，点击即可发邮件。"
    },
    {
      match: function (t) { return /名字|你是谁|who|介绍|about/.test(t); },
      reply: "这是 handsome feng 的个人网站，展示他的学习、生活和娱乐三个方面的内容。我是站内的 AI 助手，随时可以帮你解答问题！"
    },
    {
      match: function (t) { return /网站|页面|结构|板块/.test(t); },
      reply: "网站分为：\n① 学习 — 编程与阅读\n② 生活 — 旅行与日常\n③ 娱乐 — 游戏与休闲\n\n底部还有社交媒体和 Gmail 联系方式。"
    }
  ];

  function localReply(text) {
    var t = text.toLowerCase();
    for (var i = 0; i < localReplies.length; i++) {
      if (localReplies[i].match(t)) return localReplies[i].reply;
    }
    return "这个问题我暂时还不太确定 😅 你可以试试问我：\n· 网站有哪些板块？\n· 怎么联系 handsome feng？\n· 学习板块是做什么的？\n\n如需完整 AI 能力，主人可以在 js/config.js 里配置 Gemini API Key。";
  }

  // ===== UI =====
  function openChat() {
    isOpen = true;
    panel.classList.add("open");
    panel.setAttribute("aria-hidden", "false");
    toggle.classList.add("active");
    if (!greeted) {
      greeted = true;
      appendMessage("bot", "嗨！我是 AI 助手，有什么想了解的可以问我 ✦");
    }
    input.focus();
  }

  function closeChat() {
    isOpen = false;
    panel.classList.remove("open");
    panel.setAttribute("aria-hidden", "true");
    toggle.classList.remove("active");
  }

  function appendMessage(role, text) {
    var div = document.createElement("div");
    div.className = "chat-msg chat-msg--" + role;
    var bubble = document.createElement("div");
    bubble.className = "chat-bubble";
    bubble.textContent = text;
    div.appendChild(bubble);
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function showTyping() {
    var div = document.createElement("div");
    div.className = "chat-msg chat-msg--bot chat-typing";
    div.id = "chatTyping";
    div.innerHTML = '<div class="chat-bubble"><span class="dot-anim"></span><span class="dot-anim"></span><span class="dot-anim"></span></div>';
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function hideTyping() {
    var el = document.getElementById("chatTyping");
    if (el) el.remove();
  }

  // ===== Gemini API =====
  function callGemini(userText) {
    var contents = history.map(function (msg) {
      return {
        role: msg.role === "user" ? "user" : "model",
        parts: [{ text: msg.text }]
      };
    });

    contents.push({ role: "user", parts: [{ text: userText }] });

    var url =
      "https://generativelanguage.googleapis.com/v1beta/models/" +
      CHAT_CONFIG.model +
      ":generateContent?key=" +
      CHAT_CONFIG.apiKey;

    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        system_instruction: {
          parts: [{ text: CHAT_CONFIG.systemPrompt }]
        },
        contents: contents
      })
    })
      .then(function (res) {
        if (!res.ok) throw new Error("API 请求失败");
        return res.json();
      })
      .then(function (data) {
        var text = data.candidates && data.candidates[0] &&
          data.candidates[0].content && data.candidates[0].content.parts &&
          data.candidates[0].content.parts[0] &&
          data.candidates[0].content.parts[0].text;
        if (!text) throw new Error("无有效回复");
        return text.trim();
      });
  }

  function simulateDelay(ms) {
    return new Promise(function (resolve) {
      setTimeout(resolve, ms);
    });
  }

  // ===== 发送消息 =====
  function sendMessage() {
    var text = input.value.trim();
    if (!text || isLoading) return;

    appendMessage("user", text);
    input.value = "";
    input.style.height = "auto";
    isLoading = true;
    sendBtn.disabled = true;
    showTyping();

    var promise;
    if (useAI) {
      promise = callGemini(text);
    } else {
      promise = simulateDelay(600 + Math.random() * 400).then(function () {
        return localReply(text);
      });
    }

    promise
      .then(function (reply) {
        hideTyping();
        appendMessage("bot", reply);
        history.push({ role: "user", text: text });
        history.push({ role: "bot", text: reply });
        if (history.length > 20) history = history.slice(-20);
      })
      .catch(function () {
        hideTyping();
        appendMessage("bot", "抱歉，我暂时无法回复。请稍后再试，或直接发邮件至 xfxfyyds@gmail.com。");
      })
      .finally(function () {
        isLoading = false;
        sendBtn.disabled = false;
        input.focus();
      });
  }

  // ===== 事件绑定 =====
  toggle.addEventListener("click", function () {
    isOpen ? closeChat() : openChat();
  });

  closeBtn.addEventListener("click", closeChat);

  sendBtn.addEventListener("click", sendMessage);

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  input.addEventListener("input", function () {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 100) + "px";
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && isOpen) closeChat();
  });

})();
