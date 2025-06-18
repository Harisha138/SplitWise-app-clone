"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { apiService, type User, type GroupDetails } from "../services/api"

const GroupList: React.FC = () => {
  const [groups, setGroups] = useState<GroupDetails[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      console.log("Loading groups and users data...")
      const [groupsData, usersData] = await Promise.all([apiService.getGroups(), apiService.getUsers()])

      console.log("Groups loaded:", groupsData)
      console.log("Users loaded:", usersData)

      setGroups(groupsData)
      setUsers(usersData)
    } catch (error) {
      console.error("Error loading data:", error)
      setError("Failed to load data. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
        <p className="mt-2 text-gray-600">Loading groups...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <p className="text-red-600">{error}</p>
          <button onClick={loadData} className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Your Groups</h1>
        <Link
          to="/create-group"
          className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
        >
          Create New Group
        </Link>
      </div>

      {groups.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 mb-4">No groups yet</div>
          <Link
            to="/create-group"
            className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
          >
            Create Your First Group
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {groups.map((group) => (
            <Link
              key={group.id}
              to={`/groups/${group.id}`}
              className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <h3 className="text-lg font-medium text-gray-900 mb-2">{group.name}</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <p>{group.members.length} members</p>
                <p className="font-medium text-green-600">${group.total_expenses.toFixed(2)} total expenses</p>
                <p className="text-xs text-gray-500">
                  {group.expenses.length} expense{group.expenses.length !== 1 ? "s" : ""}
                </p>
              </div>

              {/* Show member names */}
              <div className="mt-3 pt-3 border-t border-gray-100">
                <p className="text-xs text-gray-500 mb-1">Members:</p>
                <div className="flex flex-wrap gap-1">
                  {group.members.slice(0, 3).map((member) => (
                    <span
                      key={member.id}
                      className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800"
                    >
                      {member.user.name}
                    </span>
                  ))}
                  {group.members.length > 3 && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-600">
                      +{group.members.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Quick Stats */}
      {groups.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Stats</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{groups.length}</div>
              <div className="text-sm text-gray-500">Total Groups</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {groups.reduce((sum, group) => sum + group.expenses.length, 0)}
              </div>
              <div className="text-sm text-gray-500">Total Expenses</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                ${groups.reduce((sum, group) => sum + group.total_expenses, 0).toFixed(2)}
              </div>
              <div className="text-sm text-gray-500">Total Amount</div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions for Users */}
      {users.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {users.slice(0, 4).map((user) => (
              <Link
                key={user.id}
                to={`/users/${user.id}/balances`}
                className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50"
              >
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-medium">{user.name.charAt(0).toUpperCase()}</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{user.name}</p>
                  <p className="text-xs text-gray-500">View balances</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default GroupList
