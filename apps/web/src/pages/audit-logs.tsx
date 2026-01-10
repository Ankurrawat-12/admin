import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { api } from '@/lib/api'
import type { AuditLog, PaginatedResponse, AuditFilters, AuditAction } from '@/lib/types'
import { formatDateTime } from '@/lib/utils'

const actionColors: Record<string, 'default' | 'success' | 'warning' | 'destructive' | 'secondary'> = {
  login: 'success',
  logout: 'secondary',
  login_failed: 'destructive',
  password_change: 'warning',
  user_create: 'success',
  user_update: 'default',
  user_delete: 'destructive',
  user_role_change: 'warning',
  project_create: 'success',
  project_update: 'default',
  project_delete: 'destructive',
  project_status_change: 'warning',
}

export function AuditLogsPage() {
  const [filters, setFilters] = useState<AuditFilters>({
    page: 1,
    page_size: 20,
    search: '',
    action: undefined,
    resource_type: undefined,
  })

  const { data, isLoading } = useQuery({
    queryKey: ['audit-logs', filters],
    queryFn: () => api.get<PaginatedResponse<AuditLog>>('/audit-logs', filters),
  })

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Audit Logs</h1>
        <p className="text-muted-foreground mt-1">
          View all system activity and security events
        </p>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col gap-4 sm:flex-row">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search by request ID..."
                className="pl-9"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value, page: 1 })}
              />
            </div>
            <Select
              value={filters.action || 'all'}
              onValueChange={(value) =>
                setFilters({
                  ...filters,
                  action: value === 'all' ? undefined : (value as AuditAction),
                  page: 1,
                })
              }
            >
              <SelectTrigger className="w-full sm:w-48">
                <SelectValue placeholder="Action" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Actions</SelectItem>
                <SelectItem value="login">Login</SelectItem>
                <SelectItem value="logout">Logout</SelectItem>
                <SelectItem value="login_failed">Login Failed</SelectItem>
                <SelectItem value="user_create">User Create</SelectItem>
                <SelectItem value="user_update">User Update</SelectItem>
                <SelectItem value="user_delete">User Delete</SelectItem>
                <SelectItem value="user_role_change">Role Change</SelectItem>
                <SelectItem value="project_create">Project Create</SelectItem>
                <SelectItem value="project_update">Project Update</SelectItem>
                <SelectItem value="project_delete">Project Delete</SelectItem>
              </SelectContent>
            </Select>
            <Select
              value={filters.resource_type || 'all'}
              onValueChange={(value) =>
                setFilters({
                  ...filters,
                  resource_type: value === 'all' ? undefined : value,
                  page: 1,
                })
              }
            >
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Resource" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Resources</SelectItem>
                <SelectItem value="auth">Auth</SelectItem>
                <SelectItem value="user">User</SelectItem>
                <SelectItem value="project">Project</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Timestamp</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>User</TableHead>
                <TableHead>Resource</TableHead>
                <TableHead>IP Address</TableHead>
                <TableHead>Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                [...Array(10)].map((_, i) => (
                  <TableRow key={i}>
                    {[...Array(6)].map((_, j) => (
                      <TableCell key={j}>
                        <Skeleton className="h-4 w-full" />
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : data?.items.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-12">
                    <FileText className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <p className="text-muted-foreground">No audit logs found</p>
                  </TableCell>
                </TableRow>
              ) : (
                data?.items.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="whitespace-nowrap">
                      {formatDateTime(log.created_at)}
                    </TableCell>
                    <TableCell>
                      <Badge variant={actionColors[log.action] || 'default'}>
                        {log.action.replace(/_/g, ' ')}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {log.user_email || (
                        <span className="text-muted-foreground">System</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{log.resource_type}</Badge>
                        {log.resource_id && (
                          <span className="text-muted-foreground">
                            #{log.resource_id}
                          </span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {log.ip_address || '-'}
                    </TableCell>
                    <TableCell className="max-w-xs">
                      {log.details ? (
                        <code className="text-xs bg-muted px-2 py-1 rounded truncate block">
                          {JSON.stringify(log.details).slice(0, 50)}
                          {JSON.stringify(log.details).length > 50 && '...'}
                        </code>
                      ) : (
                        <span className="text-muted-foreground">-</span>
                      )}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Pagination */}
      {data && data.pages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {(filters.page! - 1) * filters.page_size! + 1} to{' '}
            {Math.min(filters.page! * filters.page_size!, data.total)} of {data.total}
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={filters.page === 1}
              onClick={() => setFilters({ ...filters, page: filters.page! - 1 })}
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={filters.page === data.pages}
              onClick={() => setFilters({ ...filters, page: filters.page! + 1 })}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
