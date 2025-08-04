import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from './pages/home'
import { Login } from './pages/login'
import { SignUp } from './pages/signup'
import { Preferences } from './pages/preferences'
import { Update } from './pages/update'
import { PastLists } from "./pages/pastlists"
import { CartPage } from "./pages/cart";

function App() {

    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/signup" element={<SignUp/>}/>
                <Route path="/preferences" element={<Preferences/>}/>
                <Route path="/update" element={<Update/>}/>
                <Route path="/pastlists" element={<PastLists/>}/>
                <Route path="/cart" element={<CartPage />} />
            </Routes>
        </Router>
    );
}

export default App;
