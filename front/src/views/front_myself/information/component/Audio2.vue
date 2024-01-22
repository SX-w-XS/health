<template>
  <div class="home" style="margin:1vw;">
    <Button type="success" @click="getPermission()" style="margin:1vw;">获取麦克风权限</Button>
    <br/>
    <Button type="info" @click="startRecorder()"  style="margin:1vw;">开始录音</Button>
    <Button type="info" @click="resumeRecorder()" style="margin:1vw;">继续录音</Button>
    <Button type="info" @click="pauseRecorder()" style="margin:1vw;">暂停录音</Button>
    <Button type="info" @click="stopRecorder()" style="margin:1vw;">结束录音</Button>
    <br/>
    <Button type="success" @click="playRecorder()" style="margin:1vw;">录音播放</Button>
    <Button type="success" @click="pausePlayRecorder()" style="margin:1vw;">暂停录音播放</Button>
    <Button type="success" @click="resumePlayRecorder()" style="margin:1vw;">恢复录音播放</Button>
    <Button type="success" @click="stopPlayRecorder()" style="margin:1vw;">停止录音播放</Button>
    <br/>
    <Button type="info" @click="getRecorder()" style="margin:1vw;">获取录音信息</Button>
    <Button type="error" @click="destroyRecorder()" style="margin:1vw;">销毁录音</Button>
    <Button type="info" @click="downPCM()" style="margin:1vw;">下载PCM</Button>
    <Button type="info" @click="downWAV()" style="margin:1vw;">下载WAV</Button>
    <Button type="info" @click="getMp3Data()" style="margin:1vw;">下载MP3</Button>
    <br/>

    <br/>
    <div style="width:100%;height:200px;border:1px solid red;">
      <canvas id="canvas"></canvas>
      <span style="padding: 0 10%;"></span>
      <canvas id="playChart"></canvas>
    </div>
  </div>
</template>
<script>
import Recorder from 'js-audio-recorder'
const lamejs = require('lamejs')
let recorder = new Recorder({
  sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
  sampleRate: 48000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
  numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
  // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
})
// 绑定事件-打印的是当前录音数据
recorder.onprogress = function(params) {
  // console.log('--------------START---------------')
  // console.log('录音时长(秒)', params.duration);
  // console.log('录音大小(字节)', params.fileSize);
  // console.log('录音音量百分比(%)', params.vol);
  // console.log('当前录音的总数据([DataView, DataView...])', params.data);
  // console.log('--------------END---------------')
}
export default {
  name: 'home',
  data () {
    return {
      //波浪图-录音
      drawRecordId:null,
      oCanvas : null,
      ctx : null,
      //波浪图-播放
      drawPlayId:null,
      pCanvas : null,
      pCtx : null,
    }
  },
  mounted(){
    this.startCanvas();
  },
  methods: {

    startCanvas(){
      //录音波浪
      this.oCanvas = document.getElementById('canvas');
      this.ctx = this.oCanvas.getContext("2d");
      //播放波浪
      this.pCanvas = document.getElementById('playChart');
      this.pCtx = this.pCanvas.getContext("2d");
    },

    // 开始录音
    startRecorder () {
      recorder.start().then(() => {
        this.drawRecord();//开始绘制图片
      }, (error) => {
        // 出错了
        console.log(`${error.name} : ${error.message}`);
      });
    },
    // 继续录音
    resumeRecorder () {
      recorder.resume()
    },
    // 暂停录音
    pauseRecorder () {
      recorder.pause();
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
      this.drawRecordId = null;
    },
    // 结束录音
    stopRecorder () {
      recorder.stop()
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
      this.drawRecordId = null;
    },
    // 录音播放
    playRecorder () {
      recorder.play();
      this.drawPlay();//绘制波浪图
    },
    // 暂停录音播放
    pausePlayRecorder () {
      recorder.pausePlay()
    },
    // 恢复录音播放
    resumePlayRecorder () {
      recorder.resumePlay();
      this.drawPlay();//绘制波浪图
    },
    // 停止录音播放
    stopPlayRecorder () {
      recorder.stopPlay();
    },
    // 销毁录音
    destroyRecorder () {
      recorder.destroy().then(function() {
        recorder = null;
        this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
        this.drawRecordId = null;
      });
    },

    getRecorder(){
      let toltime = recorder.duration;//录音总时长
      let fileSize = recorder.fileSize;//录音总大小
      //录音结束，获取取录音数据
      let PCMBlob = recorder.getPCMBlob();//获取 PCM 数据
      let wav = recorder.getWAVBlob();//获取 WAV 数据
      let channel = recorder.getChannelData();//获取左声道和右声道音频数据
    },

    //下载pcm
    downPCM(){
      //这里传参进去的时文件名
      recorder.downloadPCM('新文件');
    },
    //下载wav
    downWAV(){
      //这里传参进去的时文件名
      recorder.downloadWAV('新文件');
    },

    getPermission(){
      Recorder.getPermission().then(() => {
        this.$Message.success('获取权限成功')
      }, (error) => {
        console.log(`${error.name} : ${error.message}`);
      });
    },

    getMp3Data(){
      const mp3Blob = this.convertToMp3(recorder.getWAV());
      recorder.download(mp3Blob, 'recorder', 'mp3');
    },
    convertToMp3(wavDataView) {
      // 获取wav头信息
      const wav = lamejs.WavHeader.readHeader(wavDataView); // 此处其实可以不用去读wav头信息，毕竟有对应的config配置
      const { channels, sampleRate } = wav;
      const mp3enc = new lamejs.Mp3Encoder(channels, sampleRate, 128);
      // 获取左右通道数据
      const result = recorder.getChannelData()
      const buffer = [];
      const leftData = result.left && new Int16Array(result.left.buffer, 0, result.left.byteLength / 2);
      const rightData = result.right && new Int16Array(result.right.buffer, 0, result.right.byteLength / 2);
      const remaining = leftData.length + (rightData ? rightData.length : 0);
      const maxSamples = 1152;
      for (let i = 0; i < remaining; i += maxSamples) {
        const left = leftData.subarray(i, i + maxSamples);
        let right = null;
        let mp3buf = null;
        if (channels === 2) {
          right = rightData.subarray(i, i + maxSamples);
          mp3buf = mp3enc.encodeBuffer(left, right);
        } else {
          mp3buf = mp3enc.encodeBuffer(left);
        }
        if (mp3buf.length > 0) {
          buffer.push(mp3buf);
        }
      }
      const enc = mp3enc.flush();
      if (enc.length > 0) {
        buffer.push(enc);
      }
      return new Blob(buffer, { type: 'audio/mp3' });
    },

    drawRecord () {
      // 用requestAnimationFrame稳定60fps绘制
      this.drawRecordId = requestAnimationFrame(this.drawRecord);
      // 实时获取音频大小数据
      let dataArray = recorder.getRecordAnalyseData(),
        bufferLength = dataArray.length;
      // 填充背景色
      this.ctx.fillStyle = 'rgb(200, 200, 200)';
      this.ctx.fillRect(0, 0, this.oCanvas.width, this.oCanvas.height);
      // 设定波形绘制颜色
      this.ctx.lineWidth = 2;
      this.ctx.strokeStyle = 'rgb(0, 0, 0)';
      this.ctx.beginPath();
      var sliceWidth = this.oCanvas.width * 1.0 / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
        x = 0;          // 绘制点的x轴位置
      for (var i = 0; i < bufferLength; i++) {
        var v = dataArray[i] / 128.0;
        var y = v * this.oCanvas.height / 2;
        if (i === 0) {
          // 第一个点
          this.ctx.moveTo(x, y);
        } else {
          // 剩余的点
          this.ctx.lineTo(x, y);
        }
        // 依次平移，绘制所有点
        x += sliceWidth;
      }
      this.ctx.lineTo(this.oCanvas.width, this.oCanvas.height / 2);
      this.ctx.stroke();
    },

    drawPlay () {
      // 用requestAnimationFrame稳定60fps绘制
      this.drawPlayId = requestAnimationFrame(this.drawPlay);
      // 实时获取音频大小数据
      let dataArray = recorder.getPlayAnalyseData(),
        bufferLength = dataArray.length;
      // 填充背景色
      this.pCtx.fillStyle = 'rgb(200, 200, 200)';
      this.pCtx.fillRect(0, 0, this.pCanvas.width, this.pCanvas.height);
      // 设定波形绘制颜色
      this.pCtx.lineWidth = 2;
      this.pCtx.strokeStyle = 'rgb(0, 0, 0)';
      this.pCtx.beginPath();
      var sliceWidth = this.pCanvas.width * 1.0 / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
        x = 0;          // 绘制点的x轴位置
      for (var i = 0; i < bufferLength; i++) {
        var v = dataArray[i] / 128.0;
        var y = v * this.pCanvas.height / 2;
        if (i === 0) {
          // 第一个点
          this.pCtx.moveTo(x, y);
        } else {
          // 剩余的点
          this.pCtx.lineTo(x, y);
        }
        // 依次平移，绘制所有点
        x += sliceWidth;
      }
      this.pCtx.lineTo(this.pCanvas.width, this.pCanvas.height / 2);
      this.pCtx.stroke();
    }
  },
}
</script>
<style lang='less' scoped>
</style>
