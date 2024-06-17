import AuthForm from '@/components/AuthForm'
import React from 'react'

const Signuppage = () => {
  return (
    <AuthForm method="signup" route="/admin/signup" role="admin" />
  )
}

export default Signuppage