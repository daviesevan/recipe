import React, { useState } from 'react'
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {Link} from 'react-router-dom'
import { signupEmployee, loginAdmin } from '../../Api'
import { useToast } from "@/components/ui/use-toast"
import {useNavigate} from 'react-router-dom'
const Form = ({ method }) => {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()
    const navigate = useNavigate()
  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      if (method === 'signup') {
        const response = await signupEmployee(fullName, email, password)
        toast({
          title: "Success",
          description: response.message,
        })
        navigate('/admin/login')
      } else {
        await loginAdmin(email, password)
        toast({
          title: "Success",
          description: "Logged in successfully",
        })
        navigate('/dashboard')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="mx-auto max-w-sm mt-24">
      <CardHeader>
        <CardTitle className="text-2xl">{method === 'signup' ? 'Add Employee' : 'Employee\'s Login'}</CardTitle>
        <CardDescription>
          {method === 'signup' ? 'Create a new employee account' : 'Enter your credentials to login'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          {method === 'signup' && (
            <div className="grid gap-2">
              <Label htmlFor="fullName">Full Name</Label>
              <Input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>
          )}
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="m@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="grid gap-2">
            <div className="flex items-center">
              <Label htmlFor="password">Password</Label>
              {method === 'login' && (
                <Link to="#" className="ml-auto inline-block text-sm underline">
                  Forgot your password?
                </Link>
              )}
            </div>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Processing...' : (method === 'signup' ? 'Add Employee' : 'Login')}
          </Button>
        </form>
        {method === 'login' && (
          <div className="mt-4 text-center text-sm">
            Not an admin?{" "}
            <Link to="/admin/signup" className="underline">
              Signup Here
            </Link>
          </div>
        )}
        {method === 'signup' && (
          <div className="mt-4 text-center text-sm">
            I already have an account?{" "}
            <Link to="/admin/login" className="underline">
              Login Here
            </Link>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default Form