<template>
  <div style="margin-top: 10px">
    <div class="container">
      <el-form class="container" ref="form" :model="edit_q_Form">
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
              :percentage="percentage"
            />
          </template>

          <el-radio-group v-model="edit_q_Form[currentQuestion.question_id]" class="radio_group_myself"
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
            <el-button @click="submitAnswer">提交答案</el-button>
            <el-button @click="goToPreQuestion">上一题</el-button>
            <el-button @click="goToNextQuestion(currentQuestion.question_id)">下一题</el-button>
          </div>
        </el-card>
      </el-form>
    </div>
  </div>
</template>

<script>
// 题目接口
import { getRequest } from '@/api/baseapi'
import jsondata from '../../../../static/API.json'

const model_api = '/front/get_all2'
export default {
  data() {
    return {
      currentQuestionIndex: 0,
      edit_q_Form: {},
      percentage: 0,
      questionnaires: [],
      questionnaires_count:0,
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
  created() {
    getRequest(model_api).then((res) => {
      console.log(res.questionnaires)
      this.questions = res.questionnaires[0].questions
    })

    console.log(jsondata.questionnaires.length)

    this.questionnaires=jsondata.questionnaires
    this.questionnaires_count=this.questionnaires.length
    // 获取题目接口

  },
  methods: {
    submitAnswer() {
      console.log(this.edit_q_Form)
      console.log(this.$refs.form)
      // 点击提交自动跳转到下一题
      this.goToNextQuestion()
    },
    goToNextQuestionDiv(question_id) {
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
        this.isAnswerSubmitted = false
        this.isAnswerCorrect = false
        this.userAnswer = null
      } else {
        this.percentage = 100
        alert('测试完成，点击查看结果')
        //执行提交
      }
    },
    goToNextQuestion(question_id) {
      console.log(question_id)
      // 判断是否是最后一题，如果不是则跳转到下一题，如果是进度条变为100% 并则提示测试完成，提示查看结果
      if (this.edit_q_Form[question_id] === undefined) {
        this.$notify({
          showClose: true,
          message: '请作答该题',
          type: 'warning'
        })
        return
      }
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
        this.isAnswerSubmitted = false
        this.isAnswerCorrect = false
        this.userAnswer = null
      } else {
        this.percentage = 100
        alert('测试完成，点击查看结果')
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

<style>
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

