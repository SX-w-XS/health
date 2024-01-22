<template>
  <div>
    <el-row class="button-row">
      <el-col :span="3" style="padding-left:0px">
        <el-upload
          class="upload-demo"
          :action="testUploadURL"
          :before-upload="fileUpload"
          :on-success="handleUploadSuccess"
          :show-file-list="false"
        >
          <el-button type="default" size="large" style="background: aliceblue">测试数据上传</el-button>
          <span v-show="uploadFlag">
            <el-icon class="is-loading" style="margin-left: 13px"><Loading/></el-icon>
          </span>
        </el-upload>
      </el-col>
      <el-col :span="5">
        <el-select v-model="model_test_params.model_name" @change="model_select_change" clearable placeholder="模型选择"
                   size="large" class="test-select"
        >
          <el-option
            v-for="item in modelList"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-col>
      <el-col :span="3" :offset="0" style="padding-left: 40px">
        <el-button type="default" :disabled="clickAgain" size="large" style="background: aliceblue"
                   @click="testMultiple(1)"
        >测试单行
        </el-button>
      </el-col>
      <el-col :span="3">
        <el-button type="default" :disabled="clickAgain" size="large" style="background: aliceblue"
                   @click="testMultiple(0)"
        >测试多行
        </el-button>
      </el-col>
      <el-col :span="2" :offset="2">
        <el-select v-model="selectedType" placeholder="文件类型" size="large" class="model-select"
                   @change="handleTypeChange"
        >
          <el-option
            v-for="item in TypeList"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-col>
      <el-col :span="2" style="padding-left:28px">
        <el-button type="default" size="large" style="background: aliceblue" @click="downloadTestOutput">测试结果下载
        </el-button>
      </el-col>
      <el-col :span="2" :offset="1" style="padding-left:40px">
        <el-button type="default" size="large" style="background: aliceblue" @click="testFlash">刷新</el-button>
      </el-col>

    </el-row>

    <el-row>
      <!--      训练数据列表-->
      <el-col :span="7">
        <el-table
          height="800px"
          :selectable="false"
          :stripe="true"
          :data="testList"
          @selection-change="handleSelectFileChange"
          style="width: 100%"
        >
          <el-table-column type="selection" width="55"/>
          <el-table-column label="文件" width="600px">
            <template #default="scope">{{ scope.row }}</template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="5">
        <div class="title-container">
          <p class="test-p" style="padding-left: 160px;">测试结果</p>
        </div>
        <el-input class="test-textarea"
                  v-loading="inputLoading"
                  v-model="TestJsonData"
                  :rows="10"
                  type="textarea"
                  placeholder="暂无测试结果"
        />
      </el-col>
      <!-- 饼状图-->
      <el-col :span="10" :offset="2">
        <el-row>
          <el-input placeholder="输入ID查看故障分布概率" :disabled="inputIdDisable" v-model="selectedLabelId"
                    class="test-rare-input"
                    @input="getLabelRate"
          >
          </el-input>
        </el-row>
        <!--  单次测试分布饼状图-->
        <div class="title-container">
          <p class="test-p">单条故障概率 (ID:{{ SingleId }})</p>
        </div>
        <div class="test-label-charts" ref="oneLabelChart"></div>

        <div class="title-container">
          <p class="test-p">总故障统计 (总数:{{ testCount }})</p>
        </div>
        <!--      总分布饼状图-->
        <div class="test-label-charts" ref="labelChartList"></div>
      </el-col>
    </el-row>

  </div>
</template>
<script>

import { encodeQueryParams, getModelTrain_axios, postRequest, postRequestDownload_axios } from '@/api/baseapi'
import { Message } from 'element-ui'
import * as echarts from 'echarts'
import { saveAs } from 'file-saver';
const modelApi = '/algorithm/'
const host = process.env.VUE_APP_BASE_API
const file_upload_action = host + '/algorithm/upload_file?filetype=test'

export default {
  name: 'test',
  data() {
    return {
      this_page_name: 'test',

      testCount: 0,
      jsonPath: '',
      csvPath: '',
      SingleId: '',

      inputLoading: false,
      inputIdDisable: false,
      selectedLabelId: 0,
      selectedFileRows: [],
      //文件上传地址
      testUploadURL: file_upload_action,
      selectedModel: '',
      uploadFlag: false,
      clickAgain: false,
      model_test_params: {
        flag: 0,
        datasetname: '',
        choose_model: 0,
        model_name: '',
        single: 0
      },
      test_down_params: {
        fileName: '',
        filetype: 'resultjson'
      },
      test_result: [],
      modelList: [],
      testList: [],
      TypeList: ['json', 'csv'],
      selectedType: 'json',
      TestJsonData: '',

      rateList: [],
      labelList: [],
      rateOne: ''

    }
  },
  methods: {

    //1 校验上传csv格式
    fileUpload(file) {
      this.uploadFlag = true
      console.log(file)
      const allowedExtensions = /(\.csv|\.xlsx)$/i
      if (!allowedExtensions.test(file.name)) {
        Message.error('请上传.csv或者xlsx格式文件')
        this.uploadFlag = false
        return false
      }
      return true
    },
    //2 文件上传消息回调
    handleUploadSuccess() {
      this.uploadFlag = false
      Message.success('上传成功')
      //刷新文件列表
      this.getTestList()
    },

    getLabelRate() {
        if (this.rateList == null) {
          Message.error("请先进行测试")
          return;
        }
        if (this.selectedLabelId == null) {
          Message.error("请输入查询的id")
          return;
        }
        const mapArray = []
        let singleFlge = 0
        for (let i = 0; i < this.rateList.length; i++) {
          if (this.rateList[i].id == this.selectedLabelId) {
            singleFlge = 1
            mapArray.push(
              {value: this.rateList[i].label_0, name: '故障0'},
              {value: this.rateList[i].label_1, name: '故障1'},
              {value: this.rateList[i].label_2, name: '故障2'},
              {value: this.rateList[i].label_3, name: '故障3'},
              {value: this.rateList[i].label_4, name: '故障4'},
              {value: this.rateList[i].label_5, name: '故障5'},
            )
          }
        }
        if (singleFlge == 0) {
          // Message.error("没有找到这个id哦>_<")
          return
        }
        this.SingleId = this.selectedLabelId  //输入框id和标题id同步
        //数据格式转换，单条概率
        this.rateOne = mapArray
        this.oneLabelDisplay()
    },
    // 测试，展示返回的数据
    async testMultiple(count) {
      this.clickAgain = true //训练测试时禁用训练按钮
      if (this.selectedFileRows.length > 1) {
        // Message.error("只能选择一个文件进行训练！")
        return
      }
      this.inputLoading = true
      Message({
        type: 'info',
        message: '模型测试中...',
        icon: 'Loading'
      })

      if (this.selectedFileRows.length > 0) {
        this.model_test_params.flag = 1   //启用只有数据集
        this.model_test_params.datasetname = this.selectedFileRows[0]  //选择数据集
        this.model_test_params.single = count      //  启用单条测试

      } else {
        this.model_test_params.flag = 0
        this.model_test_params.datasetname = ''
        this.model_test_params.choose_model = 0
        this.model_test_params.model_name = ''
        this.model_test_params.single = count
      }
      await getModelTrain_axios(host + modelApi + 'model_test_all' + encodeQueryParams(this.model_test_params)).then(res => {
        console.log(res)
        //数据请求成功
        res = res.data
        if (res.error){
          let formattedStr = JSON.stringify(res, null, 2)  //json格式化
          this.TestJsonData=formattedStr
          this.clickAgain = false //测试结束，启用按钮
          return
        }
        this.test_result = res
        this.clickAgain = false //测试结束，启用按钮

        this.testCount = res.all_test_count  //测试总数
        this.jsonPath = res.json_path.file_name //保存最新一次json下载结果
        this.csvPath = res.csv_path.file_name //保存csv下载名称
        this.labelList = res.test_info.label_count_info  //保存label结果

        this.rateList = res.y_Probability  //保存id概率分布列表
        this.SingleId = this.rateList[0].id //故障饼图id和第一条结果同步
        this.selectedLabelId = this.SingleId  //输入框id和标题id同步

        let formattedStr = JSON.stringify(res.y_pred2, null, 2)  //json格式化
        if (formattedStr != null) {
          this.inputLoading = false
          Message.success('数据测试成功！')
          this.TestJsonData = formattedStr
        }
        this.huatu(count)
      }).finally(
        this.inputLoading = false
      )
    },

    huatu(count) {
      if (true) {
        //多行测试

        /* 展示总饼状图 */
        //info转化为数组
        let labelInfo = this.test_result.test_info.label_count_info
        let labelList = Object.keys(labelInfo).map(key => ({
          value: labelInfo[key],
          name: "标签"+key
        }));
        this.labelList = labelList
        this.labelDisplay()

        /* 展示单条故障概率第一条 */
        const mapArraySingle = []
        this.SingleId = this.rateList[0].id //单故障饼图id和第一条结果同步

        console.log("打印ratelist",this.rateList)
        for (let i = 0; i < this.rateList.length; i++) {
          if (this.rateList[i].id == this.SingleId) {
            mapArraySingle.push(
              { value: this.rateList[i].label_0, name: '标签0' },
              { value: this.rateList[i].label_1, name: '标签1' },
              { value: this.rateList[i].label_2, name: '标签2' },
              { value: this.rateList[i].label_3, name: '标签3' },
              { value: this.rateList[i].label_4, name: '标签4' },
              { value: this.rateList[i].label_5, name: '标签5' }
            )
          }
        }
        console.log("mapArraySingle:",mapArraySingle)
        this.rateOne = mapArraySingle
        this.oneLabelDisplay()
      }

      // if (count == 1){
      //   // 测试单行
      //   console.log('单行测试结果this.---', this.test_result)
      //   this.rateList = this.test_result.y_Probability  //保存id概率分布列表
      //   this.SingleId = this.rateList[0].id
      //   //展示单饼图
      //   const mapArraySingle = []
      //   mapArraySingle.push(
      //     { value: this.rateList[0].label_0, name: '标签0' },
      //     { value: this.rateList[0].label_1, name: '标签1' },
      //     { value: this.rateList[0].label_2, name: '标签2' },
      //     { value: this.rateList[0].label_3, name: '标签3' },
      //     { value: this.rateList[0].label_4, name: '标签4' },
      //     { value: this.rateList[0].label_5, name: '标签5' }
      //   )
      //   this.rateOne = mapArraySingle
      //   this.oneLabelDisplay()
      //
      //   // this.labelList = res.data.test_info.label_count_info  //保存label结果
      //   // let labelInfo= res.data.test_info.label_count_info
      //   // for (let i = 0; i < labelInfo.length; i++) {
      //   //   this.labelList[i] = labelInfo[i]
      //   // }
      //   // labelList = Object.keys(labelList).map(key => Number(labelList[key]))
      //   // //info2转化为map数组!!!
      //   // const mapArray = []
      //   // for (let i = 0; i < labelList.length; i++) {
      //   //   const item = labelList[i]
      //   //   const obj = { value: item, name: '故障' + i }
      //   //   mapArray.push(obj)
      //   // }
      //   let labelInfo = this.test_result.test_info.label_count_info
      //   let labelList = Object.keys(labelInfo).map(key => ({
      //     value: labelInfo[key],
      //     name: "标签"+key
      //   }));
      //   this.labelList = labelList
      //   this.labelDisplay()
      //
      // }
    },

    //标签柱状图展示
//单次饼图展示
    oneLabelDisplay() {
      console.log("rateOne+++", this.rateOne)
      const labelChart = echarts.init(this.$refs.oneLabelChart)
      const labelOption = {
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            name: '概率',
            type: 'pie',
            radius: '80%',
            data: this.rateOne,
            labelLine: {
              length: 5 // 设置较短的标签线长度
            },
            label: {
              formatter: '{b} ({d}%)'
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      labelChart.setOption(labelOption)
    },
//标签柱状图展示
    labelDisplay() {
      console.log("labelList+++", this.labelList)
      const labelChart = echarts.init(this.$refs.labelChartList)
      const labelOption = {
        // title: {
        //   text: '总饼状图',
        //   left: 'center'
        // },
        //标签
        // legend: {
        //   orient: 'vertical',
        //   left: 'left'
        // },
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            name: '标签数量',
            type: 'pie',
            radius: '80%',
            data: this.labelList,
            labelLine: {
              length: 5 // 设置较短的标签线长度
            },
            label: {
              formatter: '{b} ({d}%)'
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      // labelOption.series[0].data = labelList;
      labelChart.setOption(labelOption)
    },

    //处理文件列表选中变更
    handleSelectFileChange(row) {
      this.selectedFileRows = row
      console.log(this.selectedFileRows)
    },

    model_select_change(item) {

      if (item === '') {
        this.model_test_params.choose_model = 0
      } else {
        this.model_test_params.choose_model = 1
      }
      this.model_test_params.model_name = item

      console.log(this.model_test_params)
    },

    handleTypeChange(val) {
      if (val == 'json') {
        this.test_down_params.filetype = 'resultjson'
      } else {
        this.test_down_params.filetype = 'resultcsv'
      }
      console.log(this.test_down_params)
    },

// 测试结果下载
    downloadTestOutput() {
      let outputType = ''//下载文件名
      if (this.jsonPath == null) {
        Message.error('测试结果为空，请先进行测试')
        return
      }
      if (this.test_down_params.filetype == null || this.test_down_params.filetype == '') {
        Message.error('请选择下载文件格式')
        return
      }
      if (this.test_down_params.filetype == 'resultjson') {
        outputType = this.jsonPath
      } else {
        outputType = this.csvPath
      }

      this.test_down_params.fileName=outputType
      console.log('结果下载参数---', outputType, this.test_down_params)

      postRequestDownload_axios(host + modelApi + 'download_file' + encodeQueryParams(this.test_down_params)).then(res => {
        saveAs(res.data, outputType) // 使用 saveAs 方法保存文件到本地
      }).catch(err => {
        Message.error('下载错误')
      })

    },
    // 刷新
    async testFlash() {
      await location.reload();
    },

    show_drawg() {

    },

    // 初始化模型列表
    getModelList() {
      postRequest(modelApi + 'modellist').then(res => {
        console.log('modellist---', res)
        this.modelList = res.file_model_list.reverse()
      })
    },
    //初始化上传文件列表
    getTestList() {
      postRequest(modelApi + 'datasetlist?fileType=' + this.this_page_name).then(res => {
        console.log('filelist---', res)
        this.testList = res.file_list.reverse()
      })
    }

  },
  components: {},
  mounted() {
    this.getModelList()
    this.getTestList()
  }
}
</script>
<style scoped>
.el-table__header-wrapper .el-checkbox {
  display: none
}

.label-input {
  margin-top: 5px;
  margin-bottom: 5px;
  margin-left: 20px;
}

.test-rare-input {
  display: flex;
  justify-content: center;
  padding-left: 80px;
  margin-top: 5px;
  margin-bottom: 5px;
  width: 260px;
  margin-left: 80px;
}

.card-div {
  padding-left: 10px;
}

.box-card {
  width: 400px;
display: flex;
justify-content: center;
padding-left: 80px;
  margin-left: 20px;
}

.test-label-charts {
  justify-content: center;
  width: 100%;
  height: 200px;
}

.test-textarea {
  padding-left: 76px;
}

.test-p {
  font-size: 15px;
  display: flex;
  margin-left: -43px;
  justify-content: start;
  color: #909399;
  font-weight: bold;
}

.test-select {
  width: 220px;
}

.model-select {
  width: 120px;
  margin-left: 16px;
}

.button-row {
  display: flex;
  justify-content: start;
  /* margin-top: 2px; */
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  padding-top: 5px;
}

.title-container {
  display: flex;
  align-items: center;
  justify-content: center; /* 居中对齐 */
  margin-bottom: 10px;
  padding-left: 24px;
}

.title {
  margin: 0;
  font-size: 20px;
  color: #333;
  text-transform: uppercase;
}
</style>
