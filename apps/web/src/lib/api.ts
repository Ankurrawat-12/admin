const API_BASE = '/api/v1'

type QueryParams = Record<string, string | number | boolean | undefined | null>

interface RequestOptions extends RequestInit {
  params?: QueryParams
}

class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public data?: unknown
  ) {
    super(`API Error: ${status} ${statusText}`)
    this.name = 'ApiError'
  }
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { params, ...init } = options
  
  // Build URL with query params
  let url = `${API_BASE}${endpoint}`
  if (params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        searchParams.append(key, String(value))
      }
    })
    const queryString = searchParams.toString()
    if (queryString) {
      url += `?${queryString}`
    }
  }
  
  // Get auth token
  const token = localStorage.getItem('access_token')
  
  // Setup headers
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...init.headers,
  }
  
  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(url, {
    ...init,
    headers,
  })
  
  // Handle 401 - redirect to login
  if (response.status === 401) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
    throw new ApiError(401, 'Unauthorized')
  }
  
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new ApiError(response.status, response.statusText, data)
  }
  
  // Handle empty responses
  const text = await response.text()
  if (!text) return {} as T
  
  return JSON.parse(text)
}

export const api = {
  get: <T>(endpoint: string, params?: QueryParams) =>
    request<T>(endpoint, { method: 'GET', params }),
    
  post: <T>(endpoint: string, data?: unknown) =>
    request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),
    
  patch: <T>(endpoint: string, data?: unknown) =>
    request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    }),
    
  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: 'DELETE' }),
}

export { ApiError }
