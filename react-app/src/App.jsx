import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from './pages/home'
import { Test } from './pages/test'
import { Login } from './pages/login'
import { SignUp } from './pages/signup'

function App() {

    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home/>}/>
                <Route path="/test" element={<Test/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<SignUp/>}/>
            </Routes>
        </Router>
    );
}

export default App;
