"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"
import { apiService, type GroupDetails as GroupDetailsType, type Balance } from "../services/api"

const GroupDetails: React.FC = () => {
  const { groupId } = useParams<{ groupId: string }>()
  const [group, setGroup] = useState<GroupDetailsType | null>(null)
  const [balances, setBalances] = useState<Balance[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (groupId) {
      loadGroupData()
    }
  }, [groupId])

  const loadGroupData = async () => {
    try {
      const [groupData, balancesData] = await Promise.all([
        apiService.getGroup(Number(groupId)),
        apiService.getGroupBalances(Number(groupId)),
      ])
      setGroup(groupData)
      setBalances(balancesData)
    } catch (error) {
      console.error("Error loading group data:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (!group) {
    return <div className="text-center py-8">Group not found</div>
  }

  return (
    <div className="space-y-6">
      {/* Group Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{group.name}</h1>
            <p className="text-gray-600">
              {group.members.length} members • Total expenses: ${group.total_expenses.toFixed(2)}
            </p>
          </div>
          <Link
            to={`/groups/${groupId}/add-expense`}
            className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 inline-block"
            onClick={(e) => {
              console.log("Add Expense button clicked, navigating to:", `/groups/${groupId}/add-expense`)
            }}
          >
            Add Expense
          </Link>
        </div>
      </div>

      {/* Members */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Members</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {group.members.map((member) => (
            <div key={member.id} className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-green-600 font-medium">{member.user.name.charAt(0).toUpperCase()}</span>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">{member.user.name}</p>
                <p className="text-xs text-gray-500">{member.user.email}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Balances */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Balances</h2>
        <div className="space-y-4">
          {balances.map((balance) => (
            <div key={balance.user_id} className="border rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-medium text-gray-900">{balance.user_name}</h3>
                <span
                  className={`font-medium ${
                    balance.net_balance > 0
                      ? "text-green-600"
                      : balance.net_balance < 0
                        ? "text-red-600"
                        : "text-gray-600"
                  }`}
                >
                  {balance.net_balance > 0 ? "+" : ""}${balance.net_balance.toFixed(2)}
                </span>
              </div>

              {balance.owes_to.length > 0 && (
                <div className="text-sm text-red-600 mb-1">
                  Owes: {balance.owes_to.map((debt) => `$${debt.amount.toFixed(2)} to ${debt.user_name}`).join(", ")}
                </div>
              )}

              {balance.owed_by.length > 0 && (
                <div className="text-sm text-green-600">
                  Owed:{" "}
                  {balance.owed_by.map((credit) => `$${credit.amount.toFixed(2)} by ${credit.user_name}`).join(", ")}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Recent Expenses */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Expenses</h2>
        {group.expenses.length === 0 ? (
          <p className="text-gray-500">No expenses yet</p>
        ) : (
          <div className="space-y-3">
            {group.expenses
              .slice(-10)
              .reverse()
              .map((expense) => (
                <div key={expense.id} className="flex justify-between items-center py-2 border-b">
                  <div>
                    <p className="font-medium text-gray-900">{expense.description}</p>
                    <p className="text-sm text-gray-500">
                      Paid by {expense.payer.name} • {expense.split_type} split
                    </p>
                  </div>
                  <span className="font-medium text-gray-900">${expense.amount.toFixed(2)}</span>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default GroupDetails
