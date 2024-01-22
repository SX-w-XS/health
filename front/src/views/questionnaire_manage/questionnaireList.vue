<template>
  <div style="margin-left: 5%;margin-top: 20px">
    <el-button type="primary" @click="download_questionnaire_template">模板下载</el-button>
    <el-button type="primary" @click="addDialogFormVisible=true">添加条目</el-button>
    <!--    表格展示-->
    <div>
      <el-table
        ref="filterTable"
        border
        resizable
        :data="entities"
        height="500"
        :header-cell-style="{'text-align':'center'}"
        :cell-style="{'text-align':'center'}"
        style="width: 100%"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="40"
          fixed
        />

        <el-table-column
          prop="questionnaire_name"
          label="问卷名称"
          width="200"
          fixed
        />
        <el-table-column
          prop="questionnaire_path"
          label="保存路径"
          width="300"
        >
          <template slot-scope="scope">
            <el-tag
              type="info"
              disable-transitions
            >{{ scope.row.questionnaire_path }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column
          prop="questionnaire_file_name"
          label="文件名"
          width="300"
        >
          <template slot-scope="scope">
            <el-tag
              type="warning"
              disable-transitions
            >{{ scope.row.questionnaire_file_name }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column
          prop="questionnaire_type"
          label="文件类型"
          sortable
          width="120"
        />

        <el-table-column
          prop="questionnaire_status"
          label="文件状态"
          width="100"
        />
        <el-table-column
          prop="questionnaire_beizhu"
          label="备注"
        />
        <el-table-column
          prop="create_time"
          label="创建时间"
          sortable
          width="160"
          column-key="date"
        />
<!--        <el-table-column-->
<!--          prop="is_delete"-->
<!--          label="是否删除"-->
<!--          width="80"-->
<!--          :formatter="formatter_qestion_is_delete"-->
<!--        />-->
        <el-table-column label="操作" fixed="right" width="200">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleEdit(scope.$index, scope.row)"
            >编辑
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
            >删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!--分页显示-->
    <div class="block">
      <el-pagination
        :current-page="pageEntity.currentPage"
        :page-sizes="[10, 100, 200, 500]"
        :page-size="pageEntity.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pageEntity.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!--    编辑-->
    <el-dialog title="编辑条目信息" :visible.sync="editDialogFormVisible" width="30%" :close-on-click-modal="false">
      <el-form :model="editEntity" label-width="80px">
        <el-form-item label="问卷名称">
          <el-input v-model="editEntity.questionnaire_name" placeholder="文本内容" />
        </el-form-item>

        <el-form-item label="适用类型">
          <el-select v-model="editEntity.questionnaire_type" placeholder="适用类型" clearable autocomplete>
            <el-option label="个人信息" value="个人信息" />
            <el-option label="心理诊断" value="心理诊断" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注">
          <el-input v-model="entity.questionnaire_beizhu" type="textarea" autosize placeholder="SDS心理测量" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="editEntity.questionnaire_status" placeholder="启动状态" clearable autocomplete>
            <el-option label="启用" value="启用" />
            <el-option label="停止" value="停止" />
            <el-option label="过期" value="过期" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" align="center">
        <el-button size="big" @click="editDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" size="big" @click="updateEntity">确 定</el-button>
      </div>
    </el-dialog>
    <!--  新建-->

    <el-dialog title="新建条目信息" :visible.sync="addDialogFormVisible" width="60%" :close-on-click-modal="false">
      <el-row>
        <el-col :span="12">
          <div class="block">
            <div style="margin-top: 20%; text-align: center">
              <!--              结构化文件上传-->
            </div>
            <el-upload
              ref="upload"
              drag
              class="upload-demo"
              :action="file_upload_action"
              :on-success="handle_fileup_success"
              :on-error="handle_fileup_error"
              :auto-upload="true"
            >
              <i class="el-icon-upload" />
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            </el-upload>

          </div>
        </el-col>
        <el-col :span="12"><div class="">
          <el-form :model="entity" label-width="80px">
            <el-form-item label="问卷名称">
              <el-input v-model="entity.questionnaire_name" placeholder="文本内容" />
            </el-form-item>

            <el-form-item label="适用类型">
              <el-select v-model="entity.questionnaire_type" placeholder="适用类型" clearable autocomplete>
                <el-option label="个人信息" value="个人信息" />
                <el-option label="心理诊断" value="心理诊断" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>

            <el-form-item label="备注">
              <el-input v-model="entity.questionnaire_beizhu" type="textarea" autosize placeholder="SDS心理测量" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="entity.questionnaire_status" placeholder="启动状态" clearable autocomplete>
                <el-option label="启用" value="启用" />
                <el-option label="停止" value="停止" />
                <el-option label="过期" value="过期" />
              </el-select>
            </el-form-item>

            <el-form-item label="文件路径">
              <el-input v-model="entity.questionnaire_path" disabled type="textarea" autosize placeholder="文件路径" />
            </el-form-item>

            <el-form-item label="文件名">
              <el-input v-model="entity.questionnaire_file_name" disabled type="textarea" autosize placeholder="文件名" />
            </el-form-item>

          </el-form>
        </div></el-col>
      </el-row>

      <div slot="footer" class="dialog-footer" align="center">
        <el-button size="big" @click="addDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" size="big" @click="addEntity">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

const modelApi = '/back/model_questionaire'
const host = process.env.VUE_APP_BASE_API
const file_upload_action = host + '/front/upload_questionnaire/'
const file_download_action = host + '/back/download_questionnaire_template'
export default {
  data() {
    return {
      file_upload_action: file_upload_action,
      fileList: [],
      pageEntity: {
        total: 10000,
        currentPage: 1,
        pageSize: 10,
        skip: 0
      },
      entity: {
        questionnaire_name: '',
        questionnaire_type: '',
        questionnaire_beizhu: '',
        questionnaire_path: '',
        questionnaire_file_name: '',
        questionnaire_status: '启用',
        other: ''
      },
      editEntity: {
        id: '',
        questionnaire_type: '',
        questionnaire_name: '',
        questionnaire_path: '',
        questionnaire_file_name: '',
        other: '',
        questionnaire_status: '启用',
        is_delete: 0,
        questionnaire_beizhu: ''
      }, // 编辑实体封装
      // 实体list
      entities: [
        {
          'questionnaire_name': 'string',
          'questionnaire_type': 'string',
          'questionnaire_beizhu': 'string',
          'questionnaire_path': 'string',
          'questionnaire_file_name': 'string',
          'questionnaire_status': 'string',
          'other': '',
          'is_delete': 0,
          'id': 1,
          'create_time': '2023-10-03T13:12:17',
          'update_time': '2023-10-03T13:12:17'
        }
      ],
      filter_question_type_list: [
        { text: '语音朗读文本', value: 'texts_audio' },
        { text: '视频朗读文本', value: 'texts_video' },
        { text: '语音采访文本', value: 'questions_audio' },
        { text: '视频采访文本', value: 'questions_video' }
      ],
      filter_questionnaire_path_list: [{ text: '正面', value: '正面' }, { text: '负面', value: '负面' }, {
        text: '中性',
        value: '中性'
      }],
      // 组件控制
      addDialogFormVisible: false, // 对话框打开
      editDialogFormVisible: false, // 对话框打开
      addDialogForm_file_Visible: false,
      multipleSelection: [], // 多选
      stripe: true// 斑马纹
    }
  },
  mounted() {
    this.initEntities_getall()
    this.initEntities()
  },
  methods: {
    submitUpload() {
      this.$refs.upload.submit()
    },
    download_questionnaire_template() {
      const fileUrl = file_download_action // 文件的URL地址
      const link = document.createElement('a')
      link.href = fileUrl
      link.setAttribute('download', '模板文件')
      link.click()
    },
    handle_fileup_success(response, file, fileList) {
      if (response.msg === '上传成功') {
        this.addDialogForm_file_Visible = true
        this.entity.questionnaire_file_name = response.file_name
        this.entity.questionnaire_path = response.file_path
      } else {
        this.$message.error('上传失败')
      }
    },
    // eslint-disable-next-line handle-callback-err
    handle_fileup_error(err, file, fileList) {
      this.$message.error('上传失败')
      console.log(file, fileList)
    },
    handleSizeChange(val) {
      this.pageEntity.pageSize = val
      this.initEntities()
    },
    handleCurrentChange(val) {
      this.pageEntity.currentPage = val
      this.pageEntity.skip = this.pageEntity.pageSize * (val - 1)
      this.initEntities()
    },
    initEntities_getall() {
      const skip = 0
      this.getRequest(modelApi + '?skip=' + skip).then(res => {
        if (res) {
          this.pageEntity.total = res.length
        }
      })
    },
    initEntities() {
      this.initEntities_getall()
      const skip = this.pageEntity.skip
      const limit = this.pageEntity.pageSize
      this.getRequest(modelApi + '?skip=' + skip + '&limit=' + limit).then(res => {
        if (res) {
          this.entities = res
        }
      })
    },
    addEntity() {
      if (this.entity.questionnaire_name) {
        this.postRequest(modelApi, this.entity).then(resp => {
          if (resp) {
            this.addDialogFormVisible = false
            this.initEntities()// 添加后刷新
            this.$message({
              showClose: true,
              message: '添加成功',
              type: 'success'
            })
          }
        })
      } else {
        this.$message.error('文本内容不能为空！')
      }
    },
    updateEntity() {
      this.putRequest(modelApi + '/' + this.editEntity.id, this.editEntity).then(resp => {
        if (resp) {
          this.initEntities()
          this.editDialogFormVisible = false
          this.$message({
            showClose: true,
            message: '操作成功',
            type: 'success'
          })
        }
      })
    },
    clearInput() {
      this.entity.name = ''
      this.entity.other = ''
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    handleEdit(index, row) {
      // 弹出修改
      this.editDialogFormVisible = true
      // 获取当前ID的信息
      this.editEntity = Object.assign({}, row)

      // // this.editEntity=row;//由于是双向绑定，故即便是取消也会变化，所以使用复制
      // this.editEntity= Object.assign({},row);
      // 删除不要的属性
    },
    batchDel() {
      this.$confirm('是否批量删除' + this.multipleSelection.length + '记录?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 封装ids:  url/?ids=1&ids=2
        let ids = '?'
        this.multipleSelection.forEach(item => {
          ids += 'ids=' + item.id + '&'
        })
        // 删除该条信息
        this.delRequest(modelApi + ids).then(resp => {
          if (resp) {
            this.initEntities()// 添加后刷新
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handleDelete(index, row) {
      this.$confirm('是否删除:' + row.questionnaire_name + '?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 删除该条信息
        this.editEntity = Object.assign({}, row)
        this.editEntity.is_delete = 1
        this.updateEntity()
        // this.delRequest(modelApi + row.id).then(resp => {
        //   if (resp) {
        //     this.initEntities()// 添加后刷新
        //   }
        // })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
        console.log('已取消删除')
      })
    },

    formatter_questionnaire_type(row, column) {
      let result = '正常'
      if (row.questionnaire_type === 'texts_audio') result = '语音朗读文本'
      if (row.questionnaire_type === 'texts_video') result = '视频朗读文本'
      if (row.questionnaire_type === 'questions_audio') result = '语音采访文本'
      if (row.questionnaire_type === 'questions_video') result = '视频采访文本'
      return result
    },
    formatter_qestion_is_delete(row, column) {
      let result = '未删除'
      if (row.is_delete === 1) result = '已删除'
      if (row.is_delete === 0) result = '未删除'
      return result
    },
    filter_questionnaire_path(value, row) {
      return row.questionnaire_path === value
    },
    filter_question_type(value, row) {
      console.log(row.questionnaire_type)
      return row.questionnaire_type === value
    },
    filter_is_delete(value, row) {
      return row.is_delete === 0
    }
  }
}
</script>
