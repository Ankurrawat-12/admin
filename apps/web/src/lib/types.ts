// User types
export type UserRole = 'admin' | 'manager' | 'viewer'

export interface User {
  id: number
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at: string
  last_login: string | null
}

export interface UserCreate {
  email: string
  full_name: string
  password: string
  role: UserRole
}

export interface UserUpdate {
  email?: string
  full_name?: string
  role?: UserRole
  is_active?: boolean
}

// Project types
export type ProjectStatus = 'draft' | 'active' | 'on_hold' | 'completed' | 'archived'
export type ProjectPriority = 'low' | 'medium' | 'high' | 'critical'

export interface Project {
  id: number
  name: string
  description: string | null
  status: ProjectStatus
  priority: ProjectPriority
  budget: number | null
  start_date: string | null
  end_date: string | null
  owner_id: number
  owner: User | null
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
  status?: ProjectStatus
  priority?: ProjectPriority
  budget?: number
  start_date?: string
  end_date?: string
  owner_id?: number
}

export interface ProjectUpdate {
  name?: string
  description?: string
  status?: ProjectStatus
  priority?: ProjectPriority
  budget?: number
  start_date?: string
  end_date?: string
  owner_id?: number
}

// Audit types
export type AuditAction =
  | 'login'
  | 'logout'
  | 'login_failed'
  | 'password_change'
  | 'user_create'
  | 'user_update'
  | 'user_delete'
  | 'user_role_change'
  | 'project_create'
  | 'project_update'
  | 'project_delete'
  | 'project_status_change'

export interface AuditLog {
  id: number
  user_id: number | null
  user_email: string | null
  action: AuditAction
  resource_type: string
  resource_id: number | null
  details: Record<string, unknown> | null
  ip_address: string | null
  user_agent: string | null
  request_id: string | null
  created_at: string
}

// API Response types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface AuthResponse {
  user: User
  tokens: {
    access_token: string
    refresh_token: string
    token_type: string
  }
}

export interface StatsResponse {
  total_users: number
  total_projects: number
  active_projects: number
  recent_activity_count: number
}

// Query params types
export interface PaginationParams {
  [key: string]: string | number | boolean | undefined | null
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  search?: string
}

export interface UserFilters extends PaginationParams {
  role?: UserRole
  is_active?: boolean
}

export interface ProjectFilters extends PaginationParams {
  status?: ProjectStatus
  owner_id?: number
}

export interface AuditFilters extends PaginationParams {
  user_id?: number
  action?: AuditAction
  resource_type?: string
  start_date?: string
  end_date?: string
}
