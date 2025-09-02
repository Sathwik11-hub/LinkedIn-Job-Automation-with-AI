import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface Application {
  id: number;
  job_id: number;
  status: string;
  application_date: string;
  notes?: string;
  cover_letter?: string;
  job?: {
    title: string;
    company: string;
    location: string;
  };
}

const ApplicationTracker: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchApplications();
  }, [statusFilter]);

  const fetchApplications = async () => {
    try {
      const params = statusFilter ? { status_filter: statusFilter } : {};
      const data = await apiService.getApplications(params);
      setApplications(data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: string } = {
      pending: 'bg-yellow-100 text-yellow-800',
      applied: 'bg-blue-100 text-blue-800',
      viewed: 'bg-purple-100 text-purple-800',
      interview_requested: 'bg-green-100 text-green-800',
      interview_scheduled: 'bg-green-100 text-green-800',
      offer_received: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
      accepted: 'bg-green-100 text-green-800',
      declined: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return <div className="text-center p-8">Loading applications...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold">Application Tracker</h2>
        <div className="flex space-x-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="p-2 border border-gray-300 rounded-md"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="applied">Applied</option>
            <option value="viewed">Viewed</option>
            <option value="interview_requested">Interview Requested</option>
            <option value="rejected">Rejected</option>
          </select>
          <button className="btn-primary">Apply to More Jobs</button>
        </div>
      </div>

      {applications.length === 0 ? (
        <div className="card text-center">
          <p className="text-gray-600">No applications found.</p>
          <button className="btn-primary mt-4">Start Applying to Jobs</button>
        </div>
      ) : (
        <div className="space-y-4">
          {applications.map((application) => (
            <div key={application.id} className="card">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold">
                    {application.job?.title || 'Job Title'}
                  </h3>
                  <p className="text-gray-600">
                    {application.job?.company || 'Company'} • {application.job?.location || 'Location'}
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Applied on {formatDate(application.application_date)}
                  </p>
                  {application.notes && (
                    <p className="text-sm text-gray-700 mt-2">
                      <strong>Notes:</strong> {application.notes}
                    </p>
                  )}
                </div>
                <div className="flex flex-col items-end space-y-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(application.status)}`}>
                    {application.status.replace('_', ' ').toUpperCase()}
                  </span>
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-800 text-sm">
                      View Details
                    </button>
                    <button className="text-gray-600 hover:text-gray-800 text-sm">
                      Update Status
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Summary Stats */}
      <div className="mt-8 card">
        <h3 className="text-lg font-semibold mb-4">Application Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{applications.length}</p>
            <p className="text-sm text-gray-600">Total Applications</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-yellow-600">
              {applications.filter(app => app.status === 'pending').length}
            </p>
            <p className="text-sm text-gray-600">Pending</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">
              {applications.filter(app => ['interview_requested', 'interview_scheduled', 'offer_received'].includes(app.status)).length}
            </p>
            <p className="text-sm text-gray-600">Positive Responses</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-red-600">
              {applications.filter(app => app.status === 'rejected').length}
            </p>
            <p className="text-sm text-gray-600">Rejected</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApplicationTracker;