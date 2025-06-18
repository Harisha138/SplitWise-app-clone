"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { apiService, type GroupDetails } from "../services/api"

const AddExpense: React.FC = () => {
  const { groupId } = useParams<{ groupId: string }>()
  const navigate = useNavigate()
  const [group, setGroup] = useState<GroupDetails | null>(null)
  const [description, setDescription] = useState("")
  const [amount, setAmount] = useState("")
  const [paidBy, setPaidBy] = useState<number | "">("")
  const [splitType, setSplitType] = useState<"equal" | "percentage">("equal")
  const [percentages, setPercentages] = useState<{ [key: number]: string }>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log("AddExpense component mounted, groupId:", groupId)
    if (groupId) {
      loadGroup()
    }
  }, [groupId])

  const loadGroup = async () => {
    try {
      console.log("Loading group data for groupId:", groupId)
      const groupData = await apiService.getGroup(Number(groupId))
      console.log("Group data loaded:", groupData)
      setGroup(groupData)

      // Initialize percentages for equal split
      const equalPercentage = (100 / groupData.members.length).toFixed(2)
      const initialPercentages: { [key: number]: string } = {}
      groupData.members.forEach((member) => {
        initialPercentages[member.user_id] = equalPercentage
      })
      setPercentages(initialPercentages)
    } catch (error) {
      console.error("Error loading group:", error)
      setError("Failed to load group data. Please try again.")
    }
  }

  const handlePercentageChange = (userId: number, value: string) => {
    setPercentages((prev) => ({
      ...prev,
      [userId]: value,
    }))
  }

  const getTotalPercentage = () => {
    return Object.values(percentages).reduce((sum, val) => sum + (Number.parseFloat(val) || 0), 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Form submitted")

    if (!group || !description.trim() || !amount || paidBy === "") {
      setError("Please fill in all required fields")
      return
    }

    if (splitType === "percentage" && Math.abs(getTotalPercentage() - 100) > 0.01) {
      setError("Percentages must add up to 100%")
      return
    }

    setLoading(true)
    setError(null)

    try {
      const expenseData = {
        description: description.trim(),
        amount: Number.parseFloat(amount),
        paid_by: Number(paidBy),
        split_type: splitType,
        splits:
          splitType === "percentage"
            ? group.members.map((member) => ({
                user_id: member.user_id,
                percentage: Number.parseFloat(percentages[member.user_id] || "0"),
              }))
            : undefined,
      }

      console.log("Creating expense with data:", expenseData)
      await apiService.createExpense(Number(groupId), expenseData)
      console.log("Expense created successfully, navigating back")
      navigate(`/groups/${groupId}`)
    } catch (error) {
      console.error("Error creating expense:", error)
      setError("Failed to create expense. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  if (error && !group) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h1 className="text-xl font-bold text-red-800 mb-2">Error</h1>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate(`/groups/${groupId}`)}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  if (!group) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading group data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Add Expense to {group.name}</h1>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description *
            </label>
            <input
              type="text"
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 px-3 py-2 border"
              placeholder="What was this expense for?"
              required
            />
          </div>

          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
              Amount ($) *
            </label>
            <input
              type="number"
              id="amount"
              step="0.01"
              min="0"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 px-3 py-2 border"
              placeholder="0.00"
              required
            />
          </div>

          <div>
            <label htmlFor="paidBy" className="block text-sm font-medium text-gray-700">
              Paid by *
            </label>
            <select
              id="paidBy"
              value={paidBy}
              onChange={(e) => setPaidBy(e.target.value ? Number(e.target.value) : "")}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 px-3 py-2 border"
              required
            >
              <option value="">Select who paid</option>
              {group.members.map((member) => (
                <option key={member.user_id} value={member.user_id}>
                  {member.user.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">Split Type</label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  value="equal"
                  checked={splitType === "equal"}
                  onChange={(e) => setSplitType(e.target.value as "equal")}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-900">Split equally</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="percentage"
                  checked={splitType === "percentage"}
                  onChange={(e) => setSplitType(e.target.value as "percentage")}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-900">Split by percentage</span>
              </label>
            </div>
          </div>

          {splitType === "percentage" && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Percentage Split</label>
              <div className="space-y-3">
                {group.members.map((member) => (
                  <div key={member.user_id} className="flex items-center justify-between">
                    <span className="text-sm text-gray-900">{member.user.name}</span>
                    <div className="flex items-center">
                      <input
                        type="number"
                        step="0.01"
                        min="0"
                        max="100"
                        value={percentages[member.user_id] || ""}
                        onChange={(e) => handlePercentageChange(member.user_id, e.target.value)}
                        className="w-20 border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 text-sm px-2 py-1 border"
                      />
                      <span className="ml-1 text-sm text-gray-500">%</span>
                    </div>
                  </div>
                ))}
                <div className="text-sm text-gray-600 pt-2 border-t">
                  Total: {getTotalPercentage().toFixed(2)}%
                  {Math.abs(getTotalPercentage() - 100) > 0.01 && (
                    <span className="text-red-600 ml-2">Must equal 100%</span>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate(`/groups/${groupId}`)}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-green-600 text-white rounded-md text-sm font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Adding..." : "Add Expense"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddExpense
