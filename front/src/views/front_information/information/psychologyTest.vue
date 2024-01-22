<template>
  <div class="psychology">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane
        :label="questionExam.questionnaire_name"
        :name="String(questionExam.questionnaire_id)"
        v-for="questionExam in questionnaires"
        :key="questionExam.questionnaire_id"
      >
        <el-form label-position="top" label-width="80px" :model="editForm">
          <el-form-item
            :label="index + 1 + '.' + question.question_text"
            v-for="(question, index) in questionExam.questions"
            :key="question.question_id"
          >
            <el-radio-group v-model="editForm[question.question_id]">
              <el-radio
                :label="answer.answer_id"
                v-for="answer in question.answers"
                :key="answer.answer_id"
                >{{ answer.answer_text }}
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: "PbcodePsychologyTest",

  data() {
    return {
      editForm: {},
      activeName: "",
    };
  },
  props: ["questionnaires"],

  mounted() {},

  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
  computed: {},
  watch: {
    questionnaires: {
      handler(newVal, oldVal) {
        this.activeName = String(newVal[0].questionnaire_id);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
</style>