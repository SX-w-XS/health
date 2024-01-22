<template>
  <div style="margin-left: 5%;margin-top: 20px">
    <!--    添加显示-->
    <div>
      <el-form :inline="true" :model="entity" class="demo-form-inline">
        <el-form-item label="内容" label-width="50">
          <el-input v-model="entity.text_content" type="textarea" autosize placeholder="文本内容" />
        </el-form-item>
        <el-form-item label="适用类型">
          <el-select v-model="entity.qestion_type" placeholder="适用类型" clearable autocomplete>
            <el-option label="语音朗读文本" value="texts_audio" />
            <el-option label="视频朗读文本" value="texts_video" />
            <el-option label="语音采访文本" value="questions_audio" />
            <el-option label="视频采访文本" value="questions_video" />
          </el-select>
        </el-form-item>
        <el-form-item label="情绪类型">
          <el-select v-model="entity.emotion_type" placeholder="情绪类型" clearable autocomplete>
            <el-option label="正面" value="正面" />
            <el-option label="负面" value="负面" />
            <el-option label="中性" value="中性" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="entity.other" type="textarea" autosize placeholder="默认不写" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addEntity">添加</el-button>
        </el-form-item>
      </el-form>
    </div>
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
        />

        <el-table-column
          prop="text_content"
          label="内容"
        />
        <el-table-column
          prop="emotion_type"
          label="文本情绪"
          sortable
          width="120"
          :filters="filter_emotion_type_list"
          :filter-method="filter_emotion_type"
          filter-placement="bottom-end"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.emotion_type === '正面' ? 'primary' : 'success'"
              disable-transitions
            >{{ scope.row.emotion_type }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column
          prop="qestion_type"
          label="问题类型"
          sortable
          width="120"
          :formatter="formatter_qestion_type"
          :filters="filter_question_type_list"
          :filter-method="filter_question_type"
          filter-placement="bottom-end"
        />

        <el-table-column
          prop="qestion_status"
          label="问题状态"
          width="100"
        />
        <el-table-column
          prop="other"
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
        <el-table-column label="操作">
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
    <el-dialog title="编辑条目信息" :visible.sync="editDialogFormVisible" width="70%" :close-on-click-modal="false">
      <el-form :model="editEntity" class="demo-form-inline">
        <el-form-item label="内容" label-width="50">
          <el-input v-model="editEntity.text_content" type="textarea" autosize placeholder="文本内容" />
        </el-form-item>
        <el-form-item label="适用类型">
          <el-select v-model="editEntity.qestion_type" placeholder="适用类型" clearable autocomplete>
            <el-option label="语音朗读文本" value="texts_audio" />
            <el-option label="视频朗读文本" value="texts_video" />
            <el-option label="语音采访文本" value="questions_audio" />
            <el-option label="视频采访文本" value="questions_video" />
          </el-select>
        </el-form-item>
        <el-form-item label="情绪类型">
          <el-select v-model="editEntity.emotion_type" placeholder="情绪类型" clearable autocomplete>
            <el-option label="正面" value="正面" />
            <el-option label="负面" value="负面" />
            <el-option label="中性" value="中性" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="editEntity.other" type="textarea" autosize placeholder="默认不写" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="editEntity.qestion_status" placeholder="启动状态" clearable autocomplete>
            <el-option label="启用" value="启用" />
            <el-option label="停止" value="停止" />
            <el-option label="过期" value="过期" />
          </el-select>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="editDialogFormVisible = false">取 消</el-button>
        <el-button type="primary" size="small" @click="updateEntity">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

const modelApi = '/back/model_question_records'

export default {
  data() {
    return {
      pageEntity: {
        total: 10000,
        currentPage: 1,
        pageSize: 10,
        skip: 0
      },
      entity: {
        qestion_type: 'texts_audio',
        text_content: '',
        emotion_type: '正面',
        other: '',
        qestion_status: '启用'
      },
      editEntity: {
        id: '',
        qestion_type: 'texts_audio',
        text_content: '',
        emotion_type: '正面',
        other: '',
        qestion_status: '正常',
        is_delete: 0
      }, // 编辑实体封装
      // 实体list
      entities: [
        {
          'qestion_type': 'texts_audio',
          'text_content': '青山不改',
          'emotion_type': '正面',
          'other': '用于文本录音',
          'qestion_status': '正常',
          'is_delete': 0,
          'id': 1,
          'create_time': '2023-10-03T08:06:03',
          'update_time': '2023-10-03T08:06:03'
        }
      ],
      filter_question_type_list: [
        { text: '语音朗读文本', value: 'texts_audio' },
        { text: '视频朗读文本', value: 'texts_video' },
        { text: '语音采访文本', value: 'questions_audio' },
        { text: '视频采访文本', value: 'questions_video' }
      ],
      filter_emotion_type_list: [{ text: '正面', value: '正面' }, { text: '负面', value: '负面' }, { text: '中性', value: '中性' }],
      // 组件控制
      addDialogFormVisible: false, // 对话框打开
      editDialogFormVisible: false, // 对话框打开
      multipleSelection: [], // 多选
      stripe: true// 斑马纹
    }
  },
  mounted() {
    this.initEntities_getall()
    this.initEntities()
  },
  methods: {
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
      if (this.entity.text_content) {
        this.postRequest(modelApi, this.entity).then(resp => {
          if (resp) {
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
            message: '编辑成功',
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
      this.$confirm('是否删除:' + row.text_content + '?', '提示', {
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

    formatter_qestion_type(row, column) {
      let result = '正常'
      if (row.qestion_type === 'texts_audio') result = '语音朗读文本'
      if (row.qestion_type === 'texts_video') result = '视频朗读文本'
      if (row.qestion_type === 'questions_audio') result = '语音采访文本'
      if (row.qestion_type === 'questions_video') result = '视频采访文本'
      return result
    },
    formatter_qestion_is_delete(row, column) {
      let result = '未删除'
      if (row.is_delete === 1) result = '已删除'
      if (row.is_delete === 0) result = '未删除'
      return result
    },
    filter_emotion_type(value, row) {
      return row.emotion_type === value
    },
    filter_question_type(value, row) {
      console.log(row.qestion_type)
      return row.qestion_type === value
    },
    filter_is_delete(value, row) {
      return row.is_delete === 0
    }
  }
}
</script>
