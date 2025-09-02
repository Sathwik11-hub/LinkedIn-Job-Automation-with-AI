import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface DashboardStats {
  total_applications: number;
  pending_applications: number;
  successful_applications: number;
  success_rate: number;
  recent_applications: number;
  status_breakdown: { [key: string]: number };
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const data = await apiService.getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8">Loading dashboard...</div>;
  }

  if (!stats) {
    return <div className="text-center p-8">Error loading dashboard data</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-8">Dashboard</h2>
      
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-600">Total Applications</h3>
          <p className="text-3xl font-bold text-blue-600">{stats.total_applications}</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-600">Pending</h3>
          <p className="text-3xl font-bold text-yellow-600">{stats.pending_applications}</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-600">Successful</h3>
          <p className="text-3xl font-bold text-green-600">{stats.successful_applications}</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-600">Success Rate</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.success_rate}%</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card mb-8">
        <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
        <div className="flex flex-wrap gap-4">
          <button className="btn-primary">Search Jobs</button>
          <button className="btn-primary">Batch Apply</button>
          <button className="btn-secondary">Update Preferences</button>
          <button className="btn-secondary">View Reports</button>
        </div>
      </div>

      {/* Application Status Breakdown */}
      <div className="card">
        <h3 className="text-xl font-bold mb-4">Application Status Breakdown</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(stats.status_breakdown).map(([status, count]) => (
            <div key={status} className="text-center">
              <p className="text-2xl font-bold">{count}</p>
              <p className="text-sm text-gray-600 capitalize">{status.replace('_', ' ')}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;