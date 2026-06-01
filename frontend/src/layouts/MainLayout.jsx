import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import './MainLayout.css';

export default function MainLayout({ children }) {
  return (
    <div className="main-layout">
      <Sidebar />
      <Navbar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}
