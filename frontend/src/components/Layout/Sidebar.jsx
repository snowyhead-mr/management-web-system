import { useNavigate, Link, useLocation } from 'react-router-dom'
import { 
  Users, 
  BarChart2,
  UserPlus,
  Briefcase,
  FileText,
  DollarSign,
  Clock,
  Settings,
  LogOut,
  Grid
} from 'react-feather'

const baseMenuItems = [
  {
    icon: BarChart2,
    text: 'Bảng điều khiển',
    to: '/dashboard'
  },
  {
    icon: UserPlus,
    text: 'Quản lý nhân viên',
    to: '/employees'
  },
  {
    icon: Briefcase,
    text: 'Quản lý chức vụ',
    to: '/positions'
  },
  {
    icon: FileText,
    text: 'Danh sách hợp đồng',
    to: '/contracts'
  },
  {
    icon: DollarSign,
    text: 'Bảng kê lương',
    to: '/payroll'
  },
  {
    icon: Clock,
    text: 'Chấm công',
    to: '/attendance'
  },
  {
    icon: Grid,
    text: 'Phòng ban',
    to: '/departments'
  },
  {
    icon: Settings,
    text: 'Cài đặt',
    to: '/settings'
  }
]

const adminMenuItem = {
  icon: Users,
  text: 'Quản lý',
  to: '/admin'
};

function SidebarItem({ icon: Icon, text, to, isActive }) {
  return (
    <Link
      to={to}
      className={`flex items-center gap-3 px-6 py-3 text-sm transition-colors
                ${isActive 
                  ? 'text-white bg-white/10' 
                  : 'text-white/80 hover:text-white hover:bg-white/5'}`}
    >
      <Icon size={20} />
      <span>{text}</span>
    </Link>
  )
}

export function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const menuItems = user?.role === 'admin' 
    ? [adminMenuItem, ...baseMenuItems]
    : baseMenuItems;

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <aside className="fixed left-0 top-0 w-64 h-screen bg-[#2F6BFF] text-white flex flex-col">
      <div className="flex flex-col h-full">
        <div className="p-6">
          <h2 className="text-xl font-semibold">Quản lý nhân sự</h2>
        </div>
        
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => (
              <SidebarItem
                key={item.to}
                icon={item.icon}
                text={item.text}
                to={item.to}
                isActive={location.pathname === item.to}
              />
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-2 w-full text-sm text-white/80 
                     hover:text-white hover:bg-white/5 rounded-lg transition-colors"
          >
            <LogOut size={20} />
            <span>Đăng xuất</span>
          </button>
        </div>
      </div>
    </aside>
  )
} 