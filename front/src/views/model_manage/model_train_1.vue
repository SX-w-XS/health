<template>
    <div class="container">
      <el-row class="button-container">
        <el-col :span="7" class="train-button" align="center" style="padding-left:0px">
          <!--文件上传-->
          <el-upload
            class="upload-demo"
            :action="trainUploadURL"
            :before-upload="fileUpload"
            :on-success="handleUploadSuccess"
            :show-file-list="false"
          >
            <el-button type="default" size="large" style="background: aliceblue " @click="">上传文件</el-button>
            <span v-show="uploadFlag">
            <el-icon class="is-loading" style="margin-left: 10px"><Loading/></el-icon>
          </span>
          </el-upload>
        </el-col>
        <el-col :span="4" align="center" :offset="1" class="train-button" style="padding-left:100px">
          <el-button type="default" :disabled="trainAgain" size="large" style="background: aliceblue" @click="trainModel">一键训练</el-button>
        </el-col>
        <el-col :span="2" :offset="4" align="center" class="train-button" style="padding-right:60px">
          <el-button type="default" size="large" style="background: aliceblue" @click="downloadModel">下载模型</el-button>
        </el-col>
        <el-col :span="1" class="download-span">
        <span v-show="downloadFlag" >
          <el-icon class="is-loading" style="margin-left: 10px" v-loading="loading"></el-icon>
        </span>
        </el-col>
        <el-col :span="2" :offset="1" class="train-button" style="padding-left:20px">
          <el-button type="default" size="large" style="background: aliceblue" @click="trainFlash">刷新</el-button>
        </el-col>
      </el-row>
      <el-row>
        <!--      文件列表-->
        <el-col :span="7">
          <el-table
            :stripe="true"
            height="800px"
            :data="fileList"
            @selection-change="handleSelectFileChange"
            style="width: 100%"
          >
            <el-table-column type="selection" width="55"/>
            <el-table-column label="文件" width="600px">
              <template #default="scope">{{ scope.row }}</template>
            </el-table-column>
          </el-table>
        </el-col>
        <!--      json展示-->
        <el-col :span="8">
          <p class="train-input-title">训练结果</p>
          <el-input class="train-textarea"
                    v-loading="inputLoading"
                    lass="col-input"
                    v-model="trainJsonData"
                    :rows="11"
                    type="textarea"
                    placeholder="暂无训练数据展示"
          />
        </el-col>
        <!--      模型列表-->
        <el-col :span="8">
          <el-table class="modelTable"
                    height="800px"
                    :stripe="true"
                    :data="modelList"
                    style="width: 100%"
                    @selection-change="handleSelectModelChange">
            <el-table-column type="selection" width="55"/>
            <el-table-column label="模型" width="600px" class="table-column">
              <template #default="scope">{{ scope.row }}</template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </div>
</template>
<script>
import { Message } from 'element-ui'
import {
  encodeQueryParams, getModelTrain_axios,
  getRequest,
  postRequest,
  postRequestDownload_axios
} from '@/api/baseapi'

import { saveAs } from 'file-saver';

const modelApi = '/algorithm/'
const host = process.env.VUE_APP_BASE_API
const file_upload_action = host + '/algorithm/upload_file?filetype=train'
const file_download_action = host + '/algorithm/download_model'

export default {
  name: 'ModelTrain1',
  data() {
    return {
      //上传路径
      this_page_name:'train',
      trainUploadURL: file_upload_action,
      //训练结果未返回前禁止点击测试
      trainAgain:false,
//下载加载图标显示
      downloadFlag: false,
      inputLoading:false,
      trainJsonData : null,
      loading:false,

//上传加载图标显示
      uploadFlag : false,
//上传路径
      fileList:[],          //文件列表
      modelList:[],         //模型列表
      selectedModelRows:[],  //模型选中列表
      selectedFileRows:[],   //文件选中列表
      model_train_params:{
        flag:0,
        need_attrcount:0,
        datasetname:'',
        label_name:'label_level',
        exclude_features:''
      }
    }
  },
  computed:{

  },
  methods: {
    // 文件上传步骤
    //1 校验上传csv格式
    fileUpload  (file)  {
      this.uploadFlag = true
      console.log(file)
      const allowedExtensions = /(\.csv|\.xlsx)$/i;
      if (!allowedExtensions.test(file.name)) {
        Message.error('请上传.csv或者xlsx格式文件')
        this.uploadFlag = false
        return false;
      }
      return true;
    },
    //2 文件上传消息回调
    handleUploadSuccess  () {
      this.uploadFlag = false
      Message.success("上传成功")
      //刷新文件列表
      this.getTrainList()
    },
    //处理文件列表选中变更
    handleSelectFileChange (row) {
      this.selectedFileRows = row
      console.log( this.selectedFileRows )
    },

    //初始化上传文件列表
    getTrainList(){
      postRequest(modelApi+'datasetlist?fileType='+this.this_page_name).then(res=>{
        console.log("filelist---", res)
        this.fileList = res.file_list.reverse();
      })
    },

    // 初始化模型列表
    getModelList() {
      postRequest(modelApi+'modellist').then(res=>{
        console.log("modellist---", res)
        this.modelList = res.file_model_list.reverse();
      })
    },
    // 训练模型，展示返回的数据
    async trainModel() {
      this.trainAgain = true //训练模型时禁用训练按钮
      if (this.selectedFileRows.length > 1) {
        // Message.error("只能选择一个文件进行训练！")
        return
      }
      this.inputLoading = true
      Message({
        type: 'info',
        message: '模型训练中...',
        icon: 'Loading'
      })

      if (this.selectedFileRows.length > 0) {
        this.model_train_params.flag = 1
        this.model_train_params.datasetname = this.selectedFileRows[0]
        this.model_train_params.need_attrcount = 0    //获取的属性值
        this.model_train_params.exclude_features = '' //排除的属性
        this.model_train_params.label_name = 'label_level' //排除的属性
      } else {
        this.model_train_params.flag = 0
        this.model_train_params.datasetname = ''
        this.model_train_params.need_attrcount = 0    //获取的属性值
        this.model_train_params.exclude_features = '' //排除的属性
        this.model_train_params.label_name = 'label_level' //排除的属性
      }

      await getModelTrain_axios(host+modelApi + 'model_train_all' + encodeQueryParams(this.model_train_params)).then(
        res => {
          res=res.data
          console.log("trainData---", res)
          if (res.code == 200) {
            this.trainAgain = false
            this.inputLoading = false
            Message.success("模型训练成功！");
          } else {
            this.inputLoading = false
            Message.error("模型训练失败！")
            return
          }
          let formattedStr = JSON.stringify(res, null, 2);
          this.trainJsonData = formattedStr
          this.getModelList()
        }
      )
    },
    //下载模型
    downloadModel() {
      console.log(this.selectedModelRows)
      if (this.selectedModelRows.length > 1) {
        Message.error("只能选择一个模型下载！")
        console.log(this.selectedModelRows)
        return
      }
      let selectedModel=''

      if (this.selectedModelRows.length>0){
        selectedModel=this.selectedModelRows[0]
      }else
      {
        return
      }
      console.log('selectedModel',selectedModel)
      if (selectedModel == '' || selectedModel == undefined) {
        Message.error("请选择模型")
        return
      }
      this.downloadFlag = true

      postRequestDownload_axios(file_download_action+'?fileName='+selectedModel).then(res => {
        saveAs(res.data, selectedModel); // 使用 saveAs 方法保存文件到本地
        this.downloadFlag = false
      })
    },
    //刷新按钮
    trainFlash () {
      location.reload();
    },
    //处理模型列表选中变更
    handleSelectModelChange(row) {
      this.selectedModelRows = row
      console.log('selectedModelRows',this.selectedModelRows)
    }


  },
  components: {},
  mounted() {
    this.getTrainList(),
      this.getModelList()
  }
}
</script>
<style scoped>
.download-span{
  display: flex;
  margin-top: 14px;
  margin-left: -20px;
}
/deep/ .el-table__header-wrapper .el-checkbox {
  display: none
}

.train-textarea {
  padding-left: 15px;
  width: 430px
}

.train-input-title {
  font-size: 15px;
  display: flex;
  margin-left: 195px;
  justify-content: start;
  color: #909399;
  font-weight: bold;
}

.modelTable {

}

.col-input {
  padding-top: 5px;
  padding-left: 10px;
  width: 390px;
  margin-left: 26px;
}

body {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 设置最小高度，使布局填充整个视口 */
}

header {
  /* 头部样式 */
}

main {
  flex-grow: 1; /* 主内容区域自动填充剩余空间 */
  /* 主内容区域样式 */
}

el-table {
  background: aliceblue;
  solid-color: #ddd;
}

.train-button {
//padding: 8px; padding-top: 5px; padding-bottom: 10px;
}

.button-container {
  border-bottom: 1px solid #ddd;
//margin-left: 160px;
}

.table-column {
  text-align: center;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>
