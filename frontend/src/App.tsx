import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import CreateGroup from "./components/CreateGroup"
import GroupDetails from "./components/GroupDetails"
import AddExpense from "./components/AddExpense"
import UserBalances from "./components/UserBalances"
import GroupList from "./components/GroupList"
import UserList from "./components/UserList"
import ChatbotAdvanced from "./components/ChatbotAdvanced"

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="text-xl font-bold text-green-600">
                  Splitwise
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  to="/groups"
                  className="text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Groups
                </Link>
                <Link
                  to="/users"
                  className="text-gray-700 hover:text-green-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Users
                </Link>
                <Link
                  to="/create-group"
                  className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
                >
                  Create Group
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<GroupList />} />
            <Route path="/groups" element={<GroupList />} />
            <Route path="/users" element={<UserList />} />
            <Route path="/create-group" element={<CreateGroup />} />
            <Route path="/groups/:groupId" element={<GroupDetails />} />
            <Route path="/groups/:groupId/add-expense" element={<AddExpense />} />
            <Route path="/users/:userId/balances" element={<UserBalances />} />
          </Routes>
        </main>

        {/* Add Advanced Chatbot with context */}
        <ChatbotAdvanced />
      </div>
    </Router>
  )
}

export default App
