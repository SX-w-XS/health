<template>
  <div>
    <video ref="videoElement" autoplay></video>
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
    <button @click="startRecording">开始录像</button>
    <button @click="stopRecording">停止录像</button>
  </div>
</template>
<script>
export default {
  data() {
    return {
      mediaRecorder: null,
      chunks: [],
      curTextIndex: 0,
      curText: {},
    };
  },
  props: ["videoData"],
  watch: {
    videoData: {
      handler(newVal, oldVal) {
        this.curText = newVal[this.curTextIndex];
      },
      deep: true,
    },
    curTextIndex: {
      handler(newVal, oldVal) {
        this.curText = this.videoData[newVal];
      },
      deep: true,
    },
  },
  methods: {
    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });

        const videoElement = this.$refs.videoElement;
        videoElement.srcObject = stream;
        videoElement.play();

        this.mediaRecorder = new MediaRecorder(stream);
        this.chunks = [];
        this.mediaRecorder.ondataavailable = this.handleDataAvailable;
        this.mediaRecorder.start();
      } catch (error) {
        console.error("无法访问摄像头", error);
      }
    },
    stopRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
        this.mediaRecorder.stop();
      }
    },
    handleDataAvailable(event) {
      if (event.data.size > 0) {
        this.chunks.push(event.data);
      }
    },
    preTextIndex() {
      if (this.curTextIndex > 0) {
        this.curTextIndex--;
      }
    },
    nextTextIndex() {
      if (this.curTextIndex < this.videoData.length - 1) {
        this.curTextIndex++;
      }
    },
  },
};
</script>
<style lang="scss" scoped>
</style>