<template>
  <div class="container">
    <h2>数据收集协议</h2>
    <div class="content">
      <h3>1. 信息收集范围</h3>
      <p>我们将收集以下类型的个人信息和相关数据：</p>
      <ul>
        <li>姓名、联系方式（如电子邮件地址、电话号码等）；</li>
        <li>地理位置数据；</li>
        <li>设备信息（如操作系统、浏览器类型、IP 地址等）；</li>
        <li>网站使用情况和交互数据（如访问日期和时间、浏览页面、点击行为等）；</li>
        <li>其他您自愿提供的信息。</li>
      </ul>
      <h3>2. 信息收集目的</h3>
      <p>我们将收集和处理您的个人信息和相关数据用于以下目的：</p>
      <ul>
        <li>提供、维护和改进我们的网站和服务；</li>
        <li>向您提供个性化的用户体验和定制化内容；</li>
        <li>处理您的请求、反馈和投诉；</li>
        <li>进行数据分析和统计，以改善我们的业务决策和战略；</li>
        <li>履行法律义务或根据法律要求进行必要的处理；</li>
        <li>其他明确告知并获得您同意的目的。</li>
      </ul>
      <h3>3. 数据保密与安全</h3>

      <p>我们将采取适当的技术和组织措施来保护您的个人信息和相关数据的安全和保密性。我们将采取合理的防护措施，防止未经授权的访问、使用、披露或损坏。</p>
      <h3>4. 信息共享与转让</h3>

      <p>除非获得您的明确同意或法律另有要求，我们不会将您的个人信息和相关数据转让给任何第三方。在某些情况下，我们可能会与合作伙伴或服务提供商共享您的信息，但我们将确保他们遵守本协议中所述的数据保密和安全要求。</p>

      <h3>数据存储与处理地点</h3>
      <p>您的个人信息和相关数据可能会被存储和处理在我们所在国家或其他国家/地区的服务器上。无论数据存储和处理地点如何，我们都将采取适当的措施，确保您的信息得到妥善保护。</p>

      <h3>数据保留期限</h3>
      <p>我们将在法律要求的保留期限内保留您的个人信息和相关数据。一旦不再需要，或者您要求我们删除您的信息，我们将采取合理的步骤来安全地销毁或匿名化您的数据。</p>

      <h3>用户权利</h3>
      <p>作为用户，您拥有以下权利：</p>
      <ul>
        <li>访问和更正您的个人信息；</li>
        <li>请求删除您的个人信息，除非法律要求或合法的业务目的要求保留；</li>
        <li>撤回您的同意，并停止进一步处理您的个人信息；</li>
        <li>提出投诉，向适当的监管机构投诉我们的数据处理行为。</li>
        <li>法律适用与修订</li>
        <li>本协议受适用的隐私保护法律和规定管辖。我们保留随时修订本协议的权利。对于重大变更，我们将通过适当的方式通知您。</li>

      </ul>
      <p>请您在使用我们的网站和服务之前仔细阅读、理解并同意本协议。如果您需要进一步完善协议内容，请向法律专业人士咨询，以确保您的数据收集协议符合适用的法律要求。</p>
    </div>
    <div class="btn_contact">
      <el-button type="" @click="refuse_contact" >拒绝</el-button>
      <el-button type="primary" @click="aggre_contact" >同意</el-button>
    </div>

  </div>
</template>


<script>
export default {
  name: 'user_contact',
  data() {
    return {}
  },
  methods: {
    aggre_contact(){
      console.log("同意")
      this.$emit('go-to-next-tab');
      console.log("魔炮")
    },
    refuse_contact(){

    }
  },
  components: {}
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

h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

h3 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

p, ul {
  margin-bottom: 10px;
}

li {
  list-style-type: disc;
  margin-left: 20px;
}
.btn_contact{
  display: flex;
  flex-direction: row;
}
</style>
