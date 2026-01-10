import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { api } from '@/lib/api'
import type { User, UserCreate, UserUpdate, UserRole } from '@/lib/types'
import { toast } from '@/hooks/use-toast'

interface UserModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  user: User | null
}

interface FormData {
  email: string
  full_name: string
  password: string
  role: UserRole
}

export function UserModal({ open, onOpenChange, user }: UserModalProps) {
  const queryClient = useQueryClient()
  const isEditing = !!user

  const { register, handleSubmit, reset, setValue, watch, formState: { errors } } = useForm<FormData>({
    defaultValues: {
      email: '',
      full_name: '',
      password: '',
      role: 'viewer',
    },
  })

  useEffect(() => {
    if (user) {
      reset({
        email: user.email,
        full_name: user.full_name,
        password: '',
        role: user.role,
      })
    } else {
      reset({
        email: '',
        full_name: '',
        password: '',
        role: 'viewer',
      })
    }
  }, [user, reset])

  const createMutation = useMutation({
    mutationFn: (data: UserCreate) => api.post<User>('/users', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] })
      toast({ title: 'User created', variant: 'success' })
      onOpenChange(false)
    },
    onError: (error: any) => {
      toast({
        title: 'Failed to create user',
        description: error?.data?.detail || 'An error occurred',
        variant: 'destructive',
      })
    },
  })

  const updateMutation = useMutation({
    mutationFn: (data: UserUpdate) => api.patch<User>(`/users/${user?.id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      toast({ title: 'User updated', variant: 'success' })
      onOpenChange(false)
    },
    onError: (error: any) => {
      toast({
        title: 'Failed to update user',
        description: error?.data?.detail || 'An error occurred',
        variant: 'destructive',
      })
    },
  })

  const onSubmit = (data: FormData) => {
    if (isEditing) {
      const updateData: UserUpdate = {
        email: data.email,
        full_name: data.full_name,
        role: data.role,
      }
      updateMutation.mutate(updateData)
    } else {
      createMutation.mutate(data)
    }
  }

  const isLoading = createMutation.isPending || updateMutation.isPending

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{isEditing ? 'Edit User' : 'Create User'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="full_name">Full Name *</Label>
            <Input
              id="full_name"
              {...register('full_name', { required: 'Full name is required' })}
              placeholder="John Doe"
            />
            {errors.full_name && (
              <p className="text-sm text-destructive">{errors.full_name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email *</Label>
            <Input
              id="email"
              type="email"
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              placeholder="john@example.com"
            />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>

          {!isEditing && (
            <div className="space-y-2">
              <Label htmlFor="password">Password *</Label>
              <Input
                id="password"
                type="password"
                {...register('password', {
                  required: !isEditing ? 'Password is required' : false,
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
                placeholder="••••••••"
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
          )}

          <div className="space-y-2">
            <Label>Role</Label>
            <Select
              value={watch('role')}
              onValueChange={(value) => setValue('role', value as UserRole)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="viewer">Viewer</SelectItem>
                <SelectItem value="manager">Manager</SelectItem>
                <SelectItem value="admin">Admin</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {isEditing ? 'Update' : 'Create'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
