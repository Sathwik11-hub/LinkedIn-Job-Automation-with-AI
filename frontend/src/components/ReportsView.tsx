import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface AnalyticsData {
  period_days: number;
  applications_by_date: Array<{ date: string; count: number }>;
  top_companies: Array<{ company: string; applications: number }>;
  job_types: Array<{ type: string; count: number }>;
}

const ReportsView: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [period, setPeriod] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, [period]);

  const fetchAnalytics = async () => {
    try {
      const data = await apiService.getAnalytics(period);
      setAnalytics(data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8">Loading reports...</div>;
  }

  if (!analytics) {
    return <div className="text-center p-8">Error loading analytics data</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold">Reports & Analytics</h2>
        <select
          value={period}
          onChange={(e) => setPeriod(Number(e.target.value))}
          className="p-2 border border-gray-300 rounded-md"
        >
          <option value={7}>Last 7 days</option>
          <option value={30}>Last 30 days</option>
          <option value={90}>Last 90 days</option>
          <option value={365}>Last year</option>
        </select>
      </div>

      {/* Applications Timeline */}
      <div className="card mb-8">
        <h3 className="text-xl font-bold mb-4">Applications Over Time</h3>
        <div className="h-64 flex items-end space-x-2">
          {analytics.applications_by_date.map((item, index) => (
            <div key={index} className="flex-1 flex flex-col items-center">
              <div
                className="bg-blue-500 w-full rounded-t"
                style={{
                  height: `${(item.count / Math.max(...analytics.applications_by_date.map(d => d.count)) * 200)}px`,
                  minHeight: '4px'
                }}
              ></div>
              <div className="text-xs text-gray-600 mt-2 transform -rotate-45">
                {new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </div>
              <div className="text-xs font-semibold">{item.count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Top Companies */}
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Top Companies Applied To</h3>
          <div className="space-y-3">
            {analytics.top_companies.slice(0, 10).map((company, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-gray-800">{company.company}</span>
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{
                        width: `${(company.applications / Math.max(...analytics.top_companies.map(c => c.applications)) * 100)}%`
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">{company.applications}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Job Types */}
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Job Types Distribution</h3>
          <div className="space-y-3">
            {analytics.job_types.map((jobType, index) => {
              const total = analytics.job_types.reduce((sum, item) => sum + item.count, 0);
              const percentage = total > 0 ? (jobType.count / total * 100).toFixed(1) : 0;
              
              return (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-gray-800 capitalize">
                    {jobType.type || 'Not specified'}
                  </span>
                  <div className="flex items-center">
                    <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold">
                      {jobType.count} ({percentage}%)
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="card mt-8">
        <h3 className="text-xl font-bold mb-4">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {analytics.applications_by_date.reduce((sum, item) => sum + item.count, 0)}
            </div>
            <div className="text-gray-600">Total applications in period</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {analytics.applications_by_date.length > 0 
                ? (analytics.applications_by_date.reduce((sum, item) => sum + item.count, 0) / analytics.applications_by_date.length).toFixed(1)
                : '0'
              }
            </div>
            <div className="text-gray-600">Average applications per day</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {analytics.top_companies.length}
            </div>
            <div className="text-gray-600">Companies applied to</div>
          </div>
        </div>
      </div>

      {/* Export Options */}
      <div className="card mt-8">
        <h3 className="text-xl font-bold mb-4">Export Data</h3>
        <div className="flex space-x-4">
          <button className="btn-primary">Export as CSV</button>
          <button className="btn-secondary">Export as PDF</button>
          <button className="btn-secondary">Generate Report</button>
        </div>
      </div>
    </div>
  );
};

export default ReportsView;