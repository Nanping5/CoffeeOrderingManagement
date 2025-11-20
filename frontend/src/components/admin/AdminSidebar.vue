<template>
  <div class="admin-sidebar">
    <h3>管理菜单</h3>
    <ul>
      <li>仪表板</li>
      <li>菜单管理</li>
      <li>订单管理</li>
      <li>用户管理</li>
    </ul>
    <p>功能开发中...</p>
  </div>
</template>

<script setup>
// 管理员侧边栏组件 - 开发中
</script>

<style lang="scss" scoped>
.admin-sidebar {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;

  h3 {
    margin-bottom: 15px;
    color: #333;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0 0 15px 0;

    li {
      padding: 8px 0;
      border-bottom: 1px solid #eee;
      cursor: pointer;

      &:hover {
        color: #8b4513;
      }
    }
  }
}
</style>