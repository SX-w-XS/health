<template>
  <div style="margin-left: 5%;margin-top: 20px">
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
          prop="username"
          label="用户名"
          fixed
        />

        <el-table-column
          prop="gender"
          label="性别"
          sortable
          width="60"
        />
        <el-table-column
          prop="level"
          label="学历水平"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag
              type="info"
              disable-transitions
            >{{ scope.row.level }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column
          prop="email"
          label="电子邮箱"
          width="200"
        >
          <template slot-scope="scope">
            <el-tag
              type="warning"
              disable-transitions
            >{{ scope.row.email }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column
          prop="location"
          label="位置"
        />
        <el-table-column
          label="参与状态"
        >
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>信息收集: {{ scope.row.is_person_questionare }}</p>
              <p>心理测量收集: {{ scope.row.is_mental_questionare }}</p>
              <p>朗读-语音: {{ scope.row.is_read_audio }}</p>
              <p>朗读-视频: {{ scope.row.is_read_video }}</p>
              <p>访谈-语音: {{ scope.row.is_interview_audio }}</p>
              <p>访谈-视频: {{ scope.row.is_interview_video }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.is_active }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>

        <el-table-column
          prop="mental_status"
          label="心理状态"
        />
        <el-table-column
          prop="is_send_mail"
          label="邮件通知"
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
        <el-table-column label="操作" fixed="right" width="260">
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
            <el-button
              size="mini"
              @click="handleSendEmail(scope.$index, scope.row)"
            >发送邮件
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

        <el-form-item label="用户名">
          <el-input v-model="editEntity.username" placeholder="用户名"/>
        </el-form-item>

        <el-form-item label="性别">
          <el-select v-model="editEntity.gender" placeholder="性别" clearable autocomplete>
            <el-option label="男" value="男"/>
            <el-option label="女" value="女"/>
            <el-option label="保密" value="保密"/>
          </el-select>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="editEntity.age" placeholder="年龄"/>
        </el-form-item>
        <el-form-item label="学历">
          <el-input v-model="editEntity.level" placeholder="学历"/>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editEntity.email" placeholder="邮箱"/>
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="editEntity.location" type="textarea" autosize placeholder="四川成都"/>
        </el-form-item>
        <el-form-item label="流程状态">
          <el-select v-model="editEntity.is_active" placeholder="当前状态" clearable autocomplete>
            <el-option label="无" value="无"/>
            <el-option label="完成收集" value="完成收集"/>
            <el-option label="正在收集" value="正在收集"/>
            <el-option label="未建立标签" value="未建立标签"/>
          </el-select>
        </el-form-item>

        <el-form-item label="个人信息收集">
          <el-tooltip :content="editEntity.is_person_questionare" placement="top">
            <el-switch v-model="editEntity.is_person_questionare" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>

        <el-form-item label="心理问卷">
          <el-tooltip :content="editEntity.is_mental_questionare" placement="top">
            <el-switch v-model="editEntity.is_mental_questionare" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="语音朗读">
          <el-tooltip :content="editEntity.is_read_audio" placement="top">
            <el-switch v-model="editEntity.is_read_audio" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="视频朗读">
          <el-tooltip :content="editEntity.is_read_video" placement="top">
            <el-switch v-model="editEntity.is_read_video" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="语音访谈">
          <el-tooltip :content="editEntity.is_interview_audio" placement="top">
            <el-switch v-model="editEntity.is_interview_audio" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>

        <el-form-item label="视频访谈">
          <el-tooltip :content="editEntity.is_interview_video" placement="top">
            <el-switch v-model="editEntity.is_interview_video" active-value="完成" inactive-value="未完成"></el-switch>
          </el-tooltip>
        </el-form-item>

        <el-form-item label="心理状态">
          <el-input v-model="editEntity.mental_status"  autosize placeholder="心理状态"/>
        </el-form-item>
        <el-form-item label="其他">
          <el-input v-model="editEntity.other" type="textarea" autosize placeholder="其他"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" align="center">
        <el-button size="big" @click="editDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" size="big" @click="updateEntity">确 定</el-button>
      </div>
    </el-dialog>
    <!--  新建-->

    <el-dialog title="新建条目信息" :visible.sync="addDialogFormVisible" width="60%" :close-on-click-modal="false">
        <el-form :model="entity" label-width="80px">

          <el-form-item label="用户名">
            <el-input v-model="entity.username" placeholder="用户名"/>
          </el-form-item>

          <el-form-item label="性别">
            <el-select v-model="entity.gender" placeholder="性别" clearable autocomplete>
              <el-option label="男" value="男"/>
              <el-option label="女" value="女"/>
              <el-option label="保密" value="保密"/>
            </el-select>
          </el-form-item>
          <el-form-item label="年龄">
            <el-input v-model="entity.age" placeholder="年龄"/>
          </el-form-item>
          <el-form-item label="学历">
            <el-input v-model="entity.level" placeholder="学历"/>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="entity.email" placeholder="邮箱"/>
          </el-form-item>
          <el-form-item label="位置">
            <el-input v-model="entity.location" type="textarea" autosize placeholder="四川成都"/>
          </el-form-item>
          <el-form-item label="流程状态">
            <el-select v-model="entity.is_active" placeholder="当前状态" clearable autocomplete>
              <el-option label="无" value="无"/>
              <el-option label="完成收集" value="完成收集"/>
              <el-option label="正在收集" value="正在收集"/>
              <el-option label="未建立标签" value="未建立标签"/>
            </el-select>
          </el-form-item>

          <el-form-item label="个人信息收集">
            <el-tooltip :content="entity.is_person_questionare" placement="top">
              <el-switch v-model="entity.is_person_questionare" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>

          <el-form-item label="心理问卷">
            <el-tooltip :content="entity.is_mental_questionare" placement="top">
              <el-switch v-model="entity.is_mental_questionare" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="语音朗读">
            <el-tooltip :content="entity.is_read_audio" placement="top">
              <el-switch v-model="entity.is_read_audio" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="视频朗读">
            <el-tooltip :content="entity.is_read_video" placement="top">
              <el-switch v-model="entity.is_read_video" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="语音访谈">
            <el-tooltip :content="entity.is_interview_audio" placement="top">
              <el-switch v-model="entity.is_interview_audio" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>

          <el-form-item label="视频访谈">
            <el-tooltip :content="entity.is_interview_video" placement="top">
              <el-switch v-model="entity.is_interview_video" active-value="完成" inactive-value="未完成"></el-switch>
            </el-tooltip>
          </el-form-item>

          <el-form-item label="心理状态">
            <el-input v-model="entity.mental_status"  autosize placeholder="心理状态"/>
          </el-form-item>
          <el-form-item label="其他">
            <el-input v-model="entity.other" type="textarea" autosize placeholder="其他"/>
          </el-form-item>
        </el-form>
       <div slot="footer" class="dialog-footer" align="center">
        <el-button size="big" @click="addDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" size="big" @click="addEntity">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

const modelApi = '/back/model_front_users'
const host = process.env.VUE_APP_BASE_API
const file_upload_action = host + '/front/upload_questionnaire/'
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
        username: '',
        gender: '',
        age: '',
        location: '',
        level: '',
        email: ''
      },
      editEntity: {
        id: '',
        gender: '',
        username: '',
        age: '',
        level: '',
        email: '',
        other: '',
        is_delete: 0,
        location: '',
        is_active: false,
        is_person_questionare: false,
        is_mental_questionare: false,
        is_read_audio: false,
        is_read_video: false,
        is_interview_audio: false,
        is_interview_video: false,
        is_send_mail: false,
        mental_status: '无'
      },

      // 编辑实体封装
      // 实体list
      entities: [
        {
          'username': '潘彬',
          'gender': '男',
          'age': '25',
          'location': '四川',
          'level': '硕士',
          'email': '65782152@qq.com',
          'is_active': false,
          'is_person_questionare': false,
          'is_mental_questionare': false,
          'is_read_audio': false,
          'is_read_video': false,
          'is_interview_audio': false,
          'is_interview_video': false,
          'is_send_mail': false,
          'mental_status': '无',
          'is_delete': 0,
          'id': 1,
          'create_time': '2023-10-03T16:20:03',
          'update_time': '2023-10-03T16:20:03'
        }
      ],
      filter_question_type_list: [
        { text: '语音朗读文本', value: 'texts_audio' },
        { text: '视频朗读文本', value: 'texts_video' },
        { text: '语音采访文本', value: 'questions_audio' },
        { text: '视频采访文本', value: 'questions_video' }
      ],
      filter_level_list: [{ text: '正面', value: '正面' }, { text: '负面', value: '负面' }, {
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
    handle_fileup_success(response, file, fileList) {
      if (response.msg === '上传成功') {
        this.addDialogForm_file_Visible = true
        this.entity.email = response.file_name
        this.entity.level = response.file_path
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
      if (this.entity.username) {
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
    handleSendEmail(index, row) {
      console.log('发送邮件')
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
      this.$confirm('是否删除:' + row.username + '?', '提示', {
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

    formatter_gender(row, column) {
      let result = '正常'
      if (row.gender === 'texts_audio') result = '语音朗读文本'
      if (row.gender === 'texts_video') result = '视频朗读文本'
      if (row.gender === 'questions_audio') result = '语音采访文本'
      if (row.gender === 'questions_video') result = '视频采访文本'
      return result
    },
    formatter_qestion_is_delete(row, column) {
      let result = '未删除'
      if (row.is_delete === 1) result = '已删除'
      if (row.is_delete === 0) result = '未删除'
      return result
    },
    filter_level(value, row) {
      return row.level === value
    },
    filter_question_type(value, row) {
      console.log(row.gender)
      return row.gender === value
    },
    filter_is_delete(value, row) {
      return row.is_delete === 0
    }
  }
}
</script>
