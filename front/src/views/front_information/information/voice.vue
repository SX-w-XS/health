<template>
  <div class="voice">
    <div class="statement">
      <div class="title">请具有感情的朗读以下语句(读一条提交一条):</div>
      <div class="auidoCon">
        {{ curText.emotion_type }}:{{ curText.text_content }}
      </div>
      <div class="nextBtn">
        <el-button size="small" type="primary" @click="preTextIndex"
          >上一条
        </el-button>
        <el-button size="small" type="primary" @click="nextTextIndex"
          >下一条
        </el-button>
      </div>
    </div>
    <div class="operate">
      <button @click="startRecording">开始录音</button>
      <button @click="stopRecording">停止录音</button>
    </div>

    <audio controls :src="audioURL"></audio>
  </div>
</template>

<script>
export default {
  name: "PbcodeVoice",

  data() {
    return {
      mediaRecorder: null,
      audioBlob: null,
      curTextIndex: 0,
      curText: {},
    };
  },
  props: ["audioData"],
  watch: {
    audioData: {
      handler(newVal, oldVal) {
        this.curText = newVal[this.curTextIndex];
      },
      deep: true,
    },
    curTextIndex: {
      handler(newVal, oldVal) {
        this.curText = this.audioData[newVal];
      },
      deep: true,
    },
  },
  async mounted() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.mediaRecorder = new MediaRecorder(stream);

    // 在 dataavailable 事件中收集录制的数据块
    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data && event.data.size > 0) {
        this.audioBlob = new Blob([event.data], { type: "audio/webm" });
      }
    };
  },
  computed: {
    audioURL() {
      return this.audioBlob ? URL.createObjectURL(this.audioBlob) : "";
    },
  },

  methods: {
    startRecording() {
      this.audioBlob = null;
      this.mediaRecorder.start();
    },
    stopRecording() {
      this.mediaRecorder.stop();
    },
    preTextIndex() {
      if (this.curTextIndex > 0) {
        this.curTextIndex--;
      }
    },
    nextTextIndex() {
      if (this.curTextIndex < this.audioData.length - 1) {
        this.curTextIndex++;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.voice {
  display: flex;
  flex-direction: column;
}
</style>