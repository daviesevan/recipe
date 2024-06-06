import AuthForm from '@/components/AuthForm'
import React from 'react'

const SignupPage = () => {
  return (
    <AuthForm route="/auth/signup" method="signup" />
  )
}

export default SignupPage