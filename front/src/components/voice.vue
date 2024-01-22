<template>
  <div class="voice">
    <button @click="startRecognition">开始识别</button>
    <button @click="stopRecognition">停止识别</button>

    <p>{{ transcript }}</p>
  </div>
</template>

<script>
//语音文字识别
export default {
  name: "PbcodeVoice",

  data() {
    return {
      recognition: null,
      transcript: "",
    };
  },

  mounted() {
    const SpeechRecognition =
      window.webkitSpeechRecognition || window.SpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.lang = "zh-CN"; // 设置语言为中文

    this.recognition.onresult = (event) => {
      console.log(event);
      const result = event.results[event.results.length - 1];
      this.transcript = result[0].transcript;
    };

    this.recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
    };
  },

  methods: {
    startRecognition() {
      this.transcript = "";
      this.recognition.start();
    },
    stopRecognition() {
      this.recognition.stop();
    },
  },
};
</script>

<style lang="scss" scoped>
</style>