import AuthForm from '@/components/AuthForm';
import React from 'react'

const AdminLoginPage = () => {
  return (
    <AuthForm route="/admin/login" method="login" role='admin' />
  )
}

export default AdminLoginPage;