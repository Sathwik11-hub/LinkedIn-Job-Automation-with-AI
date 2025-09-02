import React, { useState } from 'react';

const JobPreferences: React.FC = () => {
  const [preferences, setPreferences] = useState({
    keywords: '',
    location: '',
    jobType: '',
    experienceLevel: '',
    remoteOption: false,
    salaryMin: '',
    companySize: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Save preferences logic here
    console.log('Saving preferences:', preferences);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setPreferences(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-8">Job Preferences</h2>
      
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Keywords
              </label>
              <input
                type="text"
                name="keywords"
                value={preferences.keywords}
                onChange={handleInputChange}
                placeholder="e.g., Software Engineer, Python Developer"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                type="text"
                name="location"
                value={preferences.location}
                onChange={handleInputChange}
                placeholder="e.g., San Francisco, CA"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Type
              </label>
              <select
                name="jobType"
                value={preferences.jobType}
                onChange={handleInputChange}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Any</option>
                <option value="full-time">Full-time</option>
                <option value="part-time">Part-time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experience Level
              </label>
              <select
                name="experienceLevel"
                value={preferences.experienceLevel}
                onChange={handleInputChange}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Any</option>
                <option value="entry-level">Entry Level</option>
                <option value="mid-level">Mid Level</option>
                <option value="senior">Senior</option>
                <option value="executive">Executive</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Salary
              </label>
              <input
                type="number"
                name="salaryMin"
                value={preferences.salaryMin}
                onChange={handleInputChange}
                placeholder="e.g., 80000"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Size
              </label>
              <select
                name="companySize"
                value={preferences.companySize}
                onChange={handleInputChange}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Any</option>
                <option value="startup">Startup (1-50)</option>
                <option value="small">Small (51-200)</option>
                <option value="medium">Medium (201-1000)</option>
                <option value="large">Large (1000+)</option>
              </select>
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              name="remoteOption"
              checked={preferences.remoteOption}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-900">
              Remote work options only
            </label>
          </div>

          <div className="flex justify-end space-x-4">
            <button type="button" className="btn-secondary">
              Reset
            </button>
            <button type="submit" className="btn-primary">
              Save Preferences
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobPreferences;