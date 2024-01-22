<template xmlns="http://www.w3.org/1999/html">
  <!--  这是问卷组件  配合tab-->
  <div style="margin-top: 10px">
    <div class="container">
      <!--      <div>我是一个div{{ user.id }}</div>-->
      <el-form class="container" ref="form" :model="form_answer">
        <el-card class="box-card">
      <el-row>
        <el-col :span="12">
          <div class="grid-content">
            <div class="CallCamera">
              <!-- 下载按钮 -->
              <a id="downLoadLink" style="display: none"></a>
              <div class="video-box">
                <video ref="video" class="video_class"></video>
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="grid-content">

              <h2>
                题目 {{ currentQuestionIndex + 1 }} ：{{ currentQuestion.text_content }}
              </h2>
  <br>
            <div class="clss_progress">
              <el-progress :stroke-width="10" :percentage="percentage"></el-progress>
            </div>


            <div class="btn_class">
              <br />
              <br />
              <el-button key="1" type="button" @click="recordOrStop(currentQuestion.id)"  style="margin:1vw;">开始录制</el-button>
              <el-button key="2" type="button" @click="recordOrStop(currentQuestion.id)" style="margin:1vw;">保存并下一题</el-button>


            </div>


              <div class="submit">
<!--                <el-popconfirm style="margin-right: 10px"-->
<!--                               title="确定提交吗？"-->
<!--                               confirm-button-text="确定"-->
<!--                               cancel-button-text="取消"-->
<!--                               @confirm="submitAnswer"-->
<!--                >-->
<!--                  <el-button slot="reference">提交答案</el-button>-->
<!--                </el-popconfirm>-->
                <el-button @click="goToPreQuestion">上一题</el-button>
                <el-button @click="goToNextQuestion(currentQuestion.id)">下一题</el-button>
                <el-button key="next_btn" ref="next_btn" type="button" :disabled="next_tab_btn"  @click="completeFirstTab" >进入下一项</el-button>
                <el-button type="button"   @click="completeNextModel" >进入下一个模块</el-button>
              </div>

          </div>
        </el-col>
      </el-row>
        </el-card>
      </el-form>
    </div>
  </div>
</template>

<script>

import { encodeQueryParams, postRequest, postRequest_multipart } from '@/api/baseapi'

const modelApi = '/front/upload_recording/'

import RecordRTC from 'recordrtc'

export default {
  data() {
    return {
      record_flag:0,
      isRecord: false,
      newbolb: null,
      recorder: null,
      next_tab_btn: false ,
      currentQuestionIndex: 0,
      form_answer: {},
      mediaRecorder:null,
      form_data: {
        u_id: '',
        title_id: '',
        filetype: 'video',//audio
        muilt_type: ''
      },
      percentage: 0,
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
    this.dataSource = this.$props.dataSource
    this.user = this.$props.user
    this.tablist = this.$props.tablist
    console.log('进入video组件,打印传的值')
    console.log("this.user",this.user )
    console.log('dataSource:',this.dataSource)
    console.log("tablist",this.tablist)
    this.questions = this.dataSource

  },
  methods: {

    //2 控制页面的音视频组件// Mute a singular HTML5 element
   muteMe(elem) {
      elem.muted = true
      elem.pause()
    },
    // 静音所有的音视频
   mutePage() {
      for (const elem of document
        .querySelectorAll('video, audio')) {
        this.muteMe(elem)
      }
    },
    //1.获取相机
    async getCamera() {
      var constraints = {
        audio: true,
        video: {width: 320, height: 180}
      }
      // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {}
      }

      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          console.log("摄像头开启")
          // 摄像头开启成功
          this.mediaStreamTrack =
            typeof stream.stop === 'function' ? stream : stream.getTracks()[0]
          this.video_stream = stream
          this.recorder = RecordRTC(stream)
          this.video = this.$refs.video
          this.video.srcObject = stream
          this.video.onloadedmetadata = e => {
            this.video.play()
            this.record_flag=1; //开始录音
          }
        })
        .catch((err) => {
          console.log(err)
        })
    },

    // 3录制或暂停
    async recordOrStop(question_id) {
      if (this.isRecord) {
        this.stop()
      } else {
        // 获取相机
        await this.getCamera()
        this.mutePage()
        // await this.record(question_id)
        setTimeout(() => {
          // 方法区
          this.record(question_id)
        }, 1000)
      }
    },
    // 视频录制
    record(question_id) {
      console.log('开始记录  record')
      this.isRecord = !this.isRecord
      let mediaRecorder
      let options
      this.recordedBlobs = []
      if (typeof MediaRecorder.isTypeSupported === 'function') {
        // 根据浏览器来设置编码参数
        if (MediaRecorder.isTypeSupported('video/webm;codecs=vp9')) {
          options = {
            MimeType: 'video/webm;codecs=h264'
          }
        } else if (MediaRecorder.isTypeSupported('video/webm;codecs=h264')) {
          options = {
            MimeType: 'video/webm;codecs=h264'
          }
        } else if (MediaRecorder.isTypeSupported('video/webm;codecs=vp8')) {
          options = {
            MimeType: 'video/webm;codecs=vp8'
          }
        }
        mediaRecorder = new MediaRecorder(this.video_stream, options)
      } else {
        // console.log('isTypeSupported is not supported, using default codecs for browser');
        console.log('当前不支持isTypeSupported，使用浏览器的默认编解码器')
        mediaRecorder = new MediaRecorder(this.video_stream)
        this.mediaRecorder=mediaRecorder
      }

      mediaRecorder.start()
      // 视频录制监听事件
      mediaRecorder.ondataavailable = (e) => {
        console.log(e)
        // 录制的视频数据有效
        if (e.data && e.data.size > 0) {
          this.recordedBlobs.push(e.data)
        }
      }
      // 停止录像后增加下载视频功能，将视频流转为mp4格式
      mediaRecorder.onstop = () => {
        const blob = new Blob(this.recordedBlobs, { type: 'video/mp4' })
        this.newbolb = blob
        // this.download_local()
        //上传至后端

       this.uploadMp4Data(question_id)//上传视频
        this.goToNextQuestionDiv(question_id)//下一个题目
      }
    },
    // 停止录制
    stop() {
      if ( this.record_flag!==1){  console.log("请先视频");return}
      this.record_flag=2; //停止视频
      this.isRecord = !this.isRecord
      if (!this.video.srcObject) return
      const stream = this.video.srcObject
      const tracks = stream.getTracks()
      // 关闭摄像头和音频
      tracks.forEach((track) => {
        track.stop()
      })
    },

//上传wav录音数据
    uploadMp4Data:function(question_id) {
      console.log('使用上传当前题目id:',question_id)
      console.log('使用上传当前状态:',this.record_flag)
      if ( this.record_flag!==2){return false}
      this.record_flag=0
      // 创建一个formData对象
      let formData = new FormData()
      let mp4_Blob = this.newbolb
      // 生成视频名
      const name = `_video_${new Date().getTime()}.mp4`
      // 此处获取到blob对象后需要设置fileName满足当前项目上传需求，其它项目可直接传把blob作为file塞入formData
      //获取当时时间戳作为文件名
      const fileOfBlob = new File([mp4_Blob], name, { type: 'video/mp4' })
      formData.append('file', fileOfBlob)
      console.log(formData.get('file'))

      this.form_answer[question_id] = true
      this.form_data.u_id=this.user.id
      this.form_data.title_id=question_id
      this.form_data.muilt_type=this.muilt_type
      console.log(this.form_answer)
      console.log(this.form_data)
      postRequest_multipart(modelApi + encodeQueryParams(this.form_data), formData).then((response) => {
        console.log(response)
        this.form_answer[this.form_data.title_id] = true
      })
      return true
    },
    download_local() {
      // const blob = new Blob(this.recordedBlobs, { type: 'video/mp4' })
      const blob = this.newbolb
      this.recordedBlobs = []
      // 将视频链接转换完可以用于在浏览器上预览的本地视频
      const videoUrl = window.URL.createObjectURL(blob)
      // 设置下载链接
      document.getElementById('downLoadLink').href = videoUrl
      // 设置下载mp4格式视频
      document.getElementById('downLoadLink').download = 'media.mp4'
      document.getElementById('downLoadLink').innerHTML =
        'DownLoad video file'
      // 生成随机数字
      const rand = Math.floor(Math.random() * 1000000)
      // 生成视频名
      const name = `video${rand}.mp4`

      // setAttribute() 方法添加指定的属性，并为其赋指定的值
      document.getElementById('downLoadLink').setAttribute('download', name)
      document.getElementById('downLoadLink').setAttribute('name', name)

      const filename = name
      console.log(filename)

      // 0.5s后自动下载视频
      setTimeout(() => {
        document.getElementById('downLoadLink').click()
      }, 500)
    },
    completeNextModel() {
      this.$emit("go_to_next_menu")
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
      console.log("video当前题目id",question_id)
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
        // alert('测试完成，点击查看结果')
        console.log("没有下一题了")
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
        console.log("没有下一题了")
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

.btn_class {
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

.bg-purple-light {
  background: #e5e9f2;
}

.clss_progress{
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  width: 90%;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
  padding: 5px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -ms-flex-direction: row;
  flex-direction: column;
  -ms-flex-wrap: nowrap;
  flex-wrap: wrap;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -ms-flex-line-pack: center;
  align-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.CallCamera {
  flex-wrap: wrap;
  align-content: space-between;
}

.video-box {
  width: 100%;
  height: 400px;
  text-align: center;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  -ms-flex-line-pack: center;
  align-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.video_class {
  /*width: 600px;*/
  /*height: 400px;  */
  width: 100%;
  height: 100%;
  background-color: black;
  object-fit: fill;
  margin: auto;
}

.video_left {
  width: 100%;
  height: 555px;
  display: flex;
  flex-direction: column;
  align-content: center;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

canvas {
  width: 80%;
}

.CallCamera button {
  width: 100px;
  height: 40px;
  position: relative;
  margin: auto;
  border-radius: 15px;
  background-color: rgb(22, 204, 195);
  cursor: pointer;
  transition: 0.5s;
  top: 20px;
}

.CallCamera button:hover {
  font-size: 15px;
  background-color: rgb(255 99 71);
  color: white;
}

.img_bg_camera img {
  width: 300px;
  height: 200px;
}

</style>

