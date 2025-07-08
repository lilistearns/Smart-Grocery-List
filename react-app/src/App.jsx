import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from './pages/home'
import { Login } from './pages/login'
import { SignUp } from './pages/signup'
import { Preferences } from './pages/preferences'
import { Update } from './pages/update'

function App() {

    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<SignUp/>}/>
                <Route path="/preferences" element={<Preferences/>}/>
                <Route path="/update" element={<Update/>}/>
            </Routes>
        </Router>
    );
}

export default App;
