"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { apiService, type UserBalance } from "../services/api"

const UserBalances: React.FC = () => {
  const { userId } = useParams<{ userId: string }>()
  const [userBalance, setUserBalance] = useState<UserBalance | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (userId) {
      loadUserBalances()
    }
  }, [userId])

  const loadUserBalances = async () => {
    try {
      const balanceData = await apiService.getUserBalances(Number(userId))
      setUserBalance(balanceData)
    } catch (error) {
      console.error("Error loading user balances:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (!userBalance) {
    return <div className="text-center py-8">User not found</div>
  }

  return (
    <div className="space-y-6">
      {/* User Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <span className="text-green-600 font-bold text-xl">{userBalance.user_name.charAt(0).toUpperCase()}</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{userBalance.user_name}</h1>
            <p
              className={`text-lg font-medium ${
                userBalance.total_net_balance > 0
                  ? "text-green-600"
                  : userBalance.total_net_balance < 0
                    ? "text-red-600"
                    : "text-gray-600"
              }`}
            >
              Total Balance: {userBalance.total_net_balance > 0 ? "+" : ""}${userBalance.total_net_balance.toFixed(2)}
            </p>
          </div>
        </div>
      </div>

      {/* Group Balances */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Balances by Group</h2>
        {userBalance.groups.length === 0 ? (
          <p className="text-gray-500">Not part of any groups yet</p>
        ) : (
          <div className="space-y-4">
            {userBalance.groups.map((group) => (
              <div key={group.group_id} className="border rounded-lg p-4">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-medium text-gray-900">{group.group_name}</h3>
                  <span
                    className={`font-medium ${
                      group.net_balance > 0
                        ? "text-green-600"
                        : group.net_balance < 0
                          ? "text-red-600"
                          : "text-gray-600"
                    }`}
                  >
                    {group.net_balance > 0 ? "+" : ""}${group.net_balance.toFixed(2)}
                  </span>
                </div>

                {group.owes_to.length > 0 && (
                  <div className="mb-2">
                    <p className="text-sm font-medium text-red-600 mb-1">You owe:</p>
                    <div className="space-y-1">
                      {group.owes_to.map((debt, index) => (
                        <p key={index} className="text-sm text-red-600 ml-2">
                          ${debt.amount.toFixed(2)} to {debt.user_name}
                        </p>
                      ))}
                    </div>
                  </div>
                )}

                {group.owed_by.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-green-600 mb-1">You are owed:</p>
                    <div className="space-y-1">
                      {group.owed_by.map((credit, index) => (
                        <p key={index} className="text-sm text-green-600 ml-2">
                          ${credit.amount.toFixed(2)} by {credit.user_name}
                        </p>
                      ))}
                    </div>
                  </div>
                )}

                {group.net_balance === 0 && <p className="text-sm text-gray-500">All settled up!</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default UserBalances
