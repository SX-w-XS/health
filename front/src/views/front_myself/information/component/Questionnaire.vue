<template>
<!--  这是问卷组件  配合tab-->
  <div style="margin-top: 10px">
    <div class="container">
<!--      <div>我是一个div{{user.id}}</div>-->
      <el-form class="container" ref="form" :model="form_answer">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <h2>
                题目 {{ currentQuestionIndex + 1 }} ：{{ currentQuestion.question_text }}
              </h2>
              <div></div>
              <!--              <el-button @click="btnQuiz">结束测试</el-button>-->
            </div>
            <!-- 进度条 -->
            <el-progress
              :stroke-width="10"
              :percentage="percentage"
            />
          </template>

          <el-radio-group v-model="form_answer[currentQuestion.question_id]" class="radio_group_myself"
                          @input="goToNextQuestionDiv"
          >
            <div class="radio_hover">
              <el-radio class="radio_radio_myself"
                        v-for="answer in currentQuestion.answers"
                        :id="answer.order_id"
                        :key="answer.order_id"
                        :label="answer.answer_value"
                        border
              >
                {{ answer.answer_text }}
              </el-radio>
            </div>
          </el-radio-group>
          <div class="submit">
            <el-popconfirm style="margin-right: 10px"
              title="确定提交吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="submitAnswer"
            >
              <el-button slot="reference" >提交答案</el-button>
            </el-popconfirm>
            <el-button @click="goToPreQuestion">上一题</el-button>
            <el-button @click="goToNextQuestion(currentQuestion.question_id)">下一题</el-button>
            <el-button key="next_btn" ref="next_btn" type="button" :disabled="next_tab_btn"  @click="completeFirstTab" >进入下一项</el-button>
            <el-button type="button"   @click="completeNextModel" >进入下一个模块</el-button>
          </div>
        </el-card>
      </el-form>
    </div>
  </div>
</template>

<script>

const modelApi = '/front/post_questionnaire'
export default {
  data() {
    return {
      currentQuestionIndex: 0,
      form_answer: {},
      form_data:{},
      next_tab_btn:false,
      percentage: 0,
      questions: [
        {
          'question_order_id': 1,
          'question_id': 'q1001',
          'question_text': '头痛',
          'question_type': 'radio',
          'answers': [
            {
              'answer_text': '从无',
              'answer_value': 1,
              'order_id': 1
            },
            {
              'answer_text': '很轻',
              'answer_value': 2,
              'order_id': 2
            },
            {
              'answer_text': '中等',
              'answer_value': 3,
              'order_id': 3
            },
            {
              'answer_text': '偏重',
              'answer_value': 4,
              'order_id': 4
            },
            {
              'answer_text': '严重',
              'answer_value': 5,
              'order_id': 5
            }
          ]
        }
      ]
    }
  },
  props:['questionnaire','user','tablist'],
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
    this.questionnaire =this.$props.questionnaire
    this.user =this.$props.user
    this.tablist =this.$props.tablist
    console.log('进入Q组件,打印传的值')
    console.log(this.questionnaire)

    this.questions =this.questionnaire.questions
      },
  methods: {
    completeFirstTab() {
      this.$emit('go-to-next-tab');
      // console.log(this.tablist[1])
      // this.$emit('tabComplete', 'tab_');
    },
    completeNextModel() {
      this.$emit("go_to_next_menu")
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
      const finished_count=Object.keys(this.form_answer).length
      // 判断是否答题完成
      if (this.questions.length!==finished_count){
        this.$notify({
          showClose: true,
          message: '未答完',
          type: 'warning'
        })
        return
      }
      this.form_data['user_id']= this.user.id
      this.form_data['questionnaire_id']= this.questionnaire.id
      this.form_data['questionnaire_file_name']= this.questionnaire.questionnaire_file_name
      this.form_data['questionnaire_name']= this.questionnaire.questionnaire_name

      console.log(this.form_data)
      this.form_data['answerlist']=this.form_answer
      console.log("提交,打印实体")
      console.log(this.form_data)
      this.addEntity()
      this.$message({
        showClose: true,
        message: '请点击下一页',
        type: 'success'
      })
      this.completeFirstTab()
    },
    goToNextQuestionDiv(question_id) {
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      } else {
        this.percentage = 100
        // alert('测试完成，点击查看结果')
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

.h1 {
  margin: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  display: flex;
  width: 100%;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.radio_group_myself {
  font-size: 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  align-content: center;
  justify-content: center;
}

.radio_radio_myself {
  height: 60px;
}

.radio_hover :hover {
  background-color: #ff8c00;
}

.submit {
  padding-top: 50px;
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  justify-content: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}


.result {
  margin: 20px;
}


.input1 {
  margin: 10px;
}
</style>

