<template>
  <!--  这是问卷组件  配合tab-->
  <div style="margin-top: 10px">
    <div class="container">
<!--      <div>我是一个div{{ user.id }}</div>-->
      <el-form class="container" ref="form" :model="form_answer">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <h2>
                题目 {{ currentQuestionIndex + 1 }} ：{{ currentQuestion.text_content }}
              </h2>
              <div></div>
              <!--              <el-button @click="btnQuiz">结束测试</el-button>-->
              <div></div>

              <i class="el-icon-timer" type="primary">录音时长：{{ recorder.duration.toFixed(4) }}</i>

            </div>
            <!-- 进度条 -->
            <el-progress
              :stroke-width="10"
              :percentage="percentage"
            />
          </template>
          <div class="canvas_div">
            <div class="canvas_class">
              <canvas id="canvas" ref="audio_canvas"></canvas>
              <span style="padding: 0 2%;"></span>
              <canvas id="playChart" ref="audio_play_canvas"></canvas>
            </div>
          </div>

          <div class="btn_class">
            <br />
            <br />
            <el-button key="1" type="button" @click="startRecordAudio()"  style="margin:1vw;">开始录音</el-button>
            <el-button key="2" type="button" @click="stopRecorder()" style="margin:1vw;">结束录音</el-button>
            <el-button key="3" type="button" @click="playRecorder()" style="margin:1vw;">播放录音</el-button>
            <el-button key="4" type="button" @click="stopPlayRecorder()" style="margin:1vw;">停止播放</el-button>
            <el-button key="5" type="button" @click="goToNextQuestionDiv(currentQuestion.id)">保存并下一题</el-button>

          </div>
          <div class="submit">

            <el-button key="7" @click="goToPreQuestion">上一题</el-button>
            <el-button key="8" @click="goToNextQuestion(currentQuestion.id)">下一题</el-button>
            <el-button key="next_btn" ref="next_btn" type="button" :disabled="next_tab_btn"  @click="completeFirstTab" >进入下一项</el-button>
            <el-button type="button"   @click="completeNextModel" >进入下一个模块</el-button>
          </div>
        </el-card>
      </el-form>

    </div>
  </div>
</template>

<script>

import { encodeQueryParams, postRequest, postRequest_multipart } from '@/api/baseapi'

const modelApi = '/front/upload_recording/'
import Recorder from 'js-audio-recorder';

export default {
  data() {
    return {
      recorder: new Recorder({
        sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
        sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
        numChannels: 1, // 声道，支持 1 或 2， 默认是1
        // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
      }),
      //波浪图-录音
      drawRecordId:null,
      oCanvas : null,
      ctx : null,
      //波浪图-播放
      drawPlayId:null,
      pCanvas : null,
      pCtx : null,

      next_tab_btn: false ,
      mediaRecorder: null,
      isRecording: false,
      chunks: [],
      currentQuestionIndex: 0,
      form_answer: {},
      form_data: {
        u_id: '',
        title_id: '',
        filetype: 'audio',//audio
        muilt_type: ''
      },
      percentage: 0,
      now_question_id:0,
      questions: [
        {
          'id': 0,
          'qestion_type': 'texts_audio',
          'text_content': '请问你最近睡眠怎么样？',
          'emotion_type': '正面'
        },
        {
          'id': 19,
          'qestion_type': 'texts_audio',
          'text_content': '我爱中国',
          'emotion_type': '正面'
        },
        {
          'id': 20,
          'qestion_type': 'texts_audio',
          'text_content': '我是个好人',
          'emotion_type': '正面'
        }
      ]
    }
  },
  props: ['dataSource', 'user', 'tablist','muilt_type'],
  computed: {
    currentQuestion() {
      this.now_question_id=this.questions[this.currentQuestionIndex].id
      return this.questions[this.currentQuestionIndex]
    }
  },
  // 监听题目的变化改变进度条的值，当题目变化时，进度条的值也会变化,当提交最后一题时，进度条的值会变成100%
  watch: {
    currentQuestionIndex() {
      this.percentage = Math.round(
        (this.currentQuestionIndex / this.questions.length) * 100
      )
    }
  },

  mounted() {
    console.log('进入Audio组件,打印传的值')
    this.startCanvas();
    this.dataSource = this.$props.dataSource
    this.user = this.$props.user
    this.tablist = this.$props.tablist

    console.log('dataSource:',this.dataSource)
    this.questions = this.dataSource
  },
  methods: {
    completeNextModel() {
      this.$emit("go_to_next_menu")
    },
    // 关于录音
    getPermission(){
      Recorder.getPermission().then(() => {
        this.$message.success('获取权限成功')
      }, (error) => {
        console.log(`${error.name} : ${error.message}`);
      });
    },
    startCanvas(){
      //录音波浪
      this.oCanvas = this.$refs.audio_canvas;
      this.ctx = this.oCanvas.getContext("2d");
      //播放波浪
      this.pCanvas = this.$refs.audio_play_canvas;
      this.pCtx = this.pCanvas.getContext("2d");
    },
//开始录音
    startRecordAudio() {
      Recorder.getPermission().then(
        () => {
          console.log("开始录音");
          this.recorder.start().then(()=>{
            this.drawRecord();//开始绘制图片
            this.record_flag=1; //开始录音
          }); // 开始录音
        },
        (error) => {
          this.$message({
            message: "请先允许该网页使用麦克风",
            type: "info",
          });
          console.log(`${error.name} : ${error.message}`);
        }
      );
    },
    // 结束录音
    stopRecorder () {
      if ( this.record_flag!==1){  console.log("请先录音");return}
      console.log("停止录音");
      this.recorder.stop()
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
      this.drawRecordId = null;
      this.record_flag=2; //记录当前是否结束录音
    },
    // 继续录音
    resumeRecorder () {
      this.recorder.resume()
    },

    // 暂停录音
    pauseRecorder () {
      this.recorder.pause();
      this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
      this.drawRecordId = null;
    },

    // 录音播放
    playRecorder () {
      if ( this.record_flag!==2){  console.log("请先录音");return}
      this.recorder.play();
      this.drawPlay();//绘制波浪图
    },

// 暂停录音播放
    pausePlayRecorder () {
      this.recorder.pausePlay()
    },
    // 恢复录音播放
    resumePlayRecorder () {
      this.recorder.resumePlay();
      this.drawPlay();//绘制波浪图
    },
    // 停止录音播放
    stopPlayRecorder () {
      if ( this.record_flag!==2){  console.log("请先录音");return}
      this.recorder.stopPlay();
    },
    // 销毁录音
    destroyRecorder () {
      this.record_flag=0;
      this.recorder.destroy().then(function() {
        this.recorder = null;
        this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
        this.drawRecordId = null;
      });
    },

    getRecorder(){
      let toltime = this.recorder.duration;//录音总时长
      let fileSize = this.recorder.fileSize;//录音总大小
      //录音结束，获取取录音数据
      let PCMBlob = this.recorder.getPCMBlob();//获取 PCM 数据
      let wav = this.recorder.getWAVBlob();//获取 WAV 数据
      let channel = this.recorder.getChannelData();//获取左声道和右声道音频数据
    },

    // mp3转换
    getMp3Daa(){
      const mp3Blob = this.convertToMp3(this.recorder.getWAV());
      this.recorder.download(mp3Blob, 'this.recorder', 'mp3');
    },
    convertToMp3(wavDataView) {
      // 获取wav头信息
      const wav = lamejs.WavHeader.readHeader(wavDataView); // 此处其实可以不用去读wav头信息，毕竟有对应的config配置
      const { channels, sampleRate } = wav;
      const mp3enc = new lamejs.Mp3Encoder(channels, sampleRate, 128);
      // 获取左右通道数据
      const result = this.recorder.getChannelData()
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

// 画图
    drawRecord () {
      // 用requestAnimationFrame稳定60fps绘制
      this.drawRecordId = requestAnimationFrame(this.drawRecord);
      // 实时获取音频大小数据
      let dataArray = this.recorder.getRecordAnalyseData(),
        bufferLength = dataArray.length;
      // 填充背景色
      this.ctx.fillStyle ='rgb(200, 200, 200)';
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
      let dataArray = this.recorder.getPlayAnalyseData(),
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
    },



    //获取WAV录音数据
    getWAVRecordAudioData() {
      var wavBlob = this.recorder.getWAVBlob();
      console.log(wavBlob);
    },
    //下载WAV录音文件
    downloadWAVRecordAudioData() {
      this.recorder.downloadWAV("badao");
    },
    //上传wav录音数据
    uploadWAVData() {
      if ( this.record_flag!==2){return false}
      this.record_flag=0
      var wavBlob = this.recorder.getWAVBlob();
      // 创建一个formData对象
      var formData = new FormData()
      // 此处获取到blob对象后需要设置fileName满足当前项目上传需求，其它项目可直接传把blob作为file塞入formData
      const newbolb = new Blob([wavBlob], { type: 'audio/wav' })
      //获取当时时间戳作为文件名
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
      formData.append('file', fileOfBlob)


      this.form_answer[this.now_question_id] = true
      this.form_data.u_id=this.user.id
      this.form_data.title_id=this.now_question_id
      this.form_data.muilt_type=this.muilt_type
      console.log(this.form_answer)
      console.log(this.form_data)
      postRequest_multipart(modelApi + encodeQueryParams(this.form_data), formData).then((response) => {
        console.log(response)
        this.form_answer[this.form_data.title_id] = true
      })
      this.destroyRecorder()

      return true
      // uploadWavData(formData).then((response) => {
      //   console.log(response);
      // });
    },
    //获取PCB录音数据
    getPCBRecordAudioData() {
      var pcmBlob = this.recorder.getPCMBlob();
      console.log(pcmBlob);
    },
    //下载PCB录音文件
    downloadPCBRecordAudioData() {
      this.recorder.downloadPCM("badao");
    },


    completeFirstTab() {
      this.$emit('go-to-next-tab');
      // console.log(this.tablist[1])
      // this.$emit('tabComplete', 'tab_')
    },
    addEntity() {
      if (this.form_data.user_id) {
        this.postRequest(modelApi, this.form_data).then(resp => {
          if (resp) {
            //更新用户信息
            this.$message({
              showClose: true,
              message: '添加成功',
              type: 'success'
            })
          }
        })
      } else {
        this.$message.error('用户信息不能为空！')
      }
    },
    submitAnswer() {
      const finished_count = Object.keys(this.form_answer).length
      // 判断是否答题完成
      if (this.questions.length !== finished_count) {
        this.$notify({
          showClose: true,
          message: '未答完',
          type: 'warning'
        })
        return
      }
      this.form_data['user_id'] = this.user.id
      this.form_data['questionnaire_id'] = this.questionnaire.id
      this.form_data['questionnaire_file_name'] = this.questionnaire.questionnaire_file_name
      this.form_data['questionnaire_name'] = this.questionnaire.questionnaire_name

      console.log(this.form_data)
      this.form_data['answerlist'] = this.form_answer
      console.log('提交,打印实体')
      console.log(this.form_data)
      this.addEntity()
      this.$message({
        showClose: true,
        message: '请点击下一页',
        type: 'success'
      })
    },
    goToNextQuestionDiv(question_id) {
      console.log("audio当前",question_id)
      this.stopRecorder()
      console.log("uploadWAVData状态：",this.uploadWAVData())
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.form_answer[question_id] === undefined) {
        this.$notify({
          showClose: true,
          message: '请作答该题',
          type: 'warning'
        })
        return
      }
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      } else {
        this.percentage = 100
        this.next_tab_btn=true
        // alert('测试完成，点击查看结果')
        this.$notify({
          showClose: true,
          message: '没有下一个题了',
          type: 'success'
        })
        //执行提交
      }
    },
    goToNextQuestion(question_id) {
      console.log(question_id)
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.form_answer[question_id] === undefined) {
        this.$notify({
          showClose: true,
          message: '请作答该题',
          type: 'warning'
        })
        return
      }
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      } else {
        this.percentage = 100
        this.$notify({
          showClose: true,
          message: '没有下一个题了',
          type: 'success'
        })
      }
    },
    goToPreQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
        this.isAnswerSubmitted = false
        this.isAnswerCorrect = false
        this.userAnswer = null
      }
    },
    btnQuiz() {
      this.quizComplete = true
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
  align-content: center;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  display: flex;
  width: 80%;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.submit {
  padding-top: 50px;
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  justify-content: center;
}

.canvas_class{
  display: flex;
  display: flex;
  width: 80%;
  height: 160px;
  border: 1px solid red;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: center;
  align-items: center;
  justify-content: center;
}
.canvas_div{
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.btn_class{
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: row;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}


</style>

