const API_BASE_URL = "http://localhost:8000" 

export interface User {
  id: number
  name: string
  email: string
  created_at: string
}

export interface Group {
  id: number
  name: string
  created_at: string
  members: GroupMember[]
}

export interface GroupMember {
  id: number
  user_id: number
  user: User
}

export interface GroupDetails extends Group {
  expenses: Expense[]
  total_expenses: number
}

export interface Expense {
  id: number
  description: string
  amount: number
  paid_by: number
  split_type: "equal" | "percentage"
  created_at: string
  payer: User
  splits: ExpenseSplit[]
}

export interface ExpenseSplit {
  id: number
  user_id: number
  amount: number
  percentage?: number
  user: User
}

export interface Balance {
  user_id: number
  user_name: string
  owes_to: Array<{ user_id: number; user_name: string; amount: number }>
  owed_by: Array<{ user_id: number; user_name: string; amount: number }>
  net_balance: number
}

export interface UserBalance {
  user_id: number
  user_name: string
  groups: Array<{
    group_id: number
    group_name: string
    net_balance: number
    owes_to: Array<{ user_id: number; user_name: string; amount: number }>
    owed_by: Array<{ user_id: number; user_name: string; amount: number }>
  }>
  total_net_balance: number
}

class ApiService {
  // Users
  async getUsers(): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/users/`)
    return response.json()
  }

  async createUser(userData: { name: string; email: string }): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    })
    return response.json()
  }

  // Groups
  async getGroups(): Promise<GroupDetails[]> {
    console.log("API: Fetching all groups")
    try {
      const response = await fetch(`${API_BASE_URL}/groups/`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      console.log("API: Groups data received", data)
      return data
    } catch (error) {
      console.error("API: Error fetching groups", error)
      throw error
    }
  }

  async createGroup(groupData: { name: string; user_ids: number[] }): Promise<Group> {
    const response = await fetch(`${API_BASE_URL}/groups/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(groupData),
    })
    return response.json()
  }

  async getGroup(groupId: number): Promise<GroupDetails> {
    console.log("API: Fetching group", groupId)
    try {
      const response = await fetch(`${API_BASE_URL}/groups/${groupId}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      console.log("API: Group data received", data)
      return data
    } catch (error) {
      console.error("API: Error fetching group", error)
      throw error
    }
  }

  // Expenses
  async createExpense(
    groupId: number,
    expenseData: {
      description: string
      amount: number
      paid_by: number
      split_type: "equal" | "percentage"
      splits?: Array<{ user_id: number; percentage?: number }>
    },
  ): Promise<Expense> {
    console.log("API: Creating expense", { groupId, expenseData })
    try {
      const response = await fetch(`${API_BASE_URL}/groups/${groupId}/expenses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(expenseData),
      })
      if (!response.ok) {
        const errorText = await response.text()
        console.error("API: Create expense failed", response.status, errorText)
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`)
      }
      const data = await response.json()
      console.log("API: Expense created successfully", data)
      return data
    } catch (error) {
      console.error("API: Error creating expense", error)
      throw error
    }
  }

  // Balances
  async getGroupBalances(groupId: number): Promise<Balance[]> {
    const response = await fetch(`${API_BASE_URL}/groups/${groupId}/balances`)
    return response.json()
  }

  async getUserBalances(userId: number): Promise<UserBalance> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/balances`)
    return response.json()
  }

  // Chatbot
  async sendChatQuery(
    query: string,
    userContext?: any,
  ): Promise<{
    query: string
    response: string
    timestamp: string
  }> {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, user_context: userContext }),
    })
    return response.json()
  }

  async getChatStats(): Promise<{
    total_users: number
    total_groups: number
    total_expenses: number
    recent_expenses: Array<{
      description: string
      amount: number
      paid_by: string
      group_name: string
      created_at: string
    }>
  }> {
    const response = await fetch(`${API_BASE_URL}/chat/stats`)
    return response.json()
  }
}

export const apiService = new ApiService()
