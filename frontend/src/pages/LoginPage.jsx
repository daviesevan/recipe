import AuthForm from '@/components/AuthForm'
import React from 'react'

const LoginPage = () => {
  return (
    <AuthForm route="/auth/login" method="login" />
  )
}

export default LoginPage