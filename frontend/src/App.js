import { AuthProvider } from "./context/AuthContext"; 
import { BrowserRouter as Router } from "react-router-dom";
import AppRouter from "./AppRouter";
import Layout from "./Layout";
import 'bootstrap/dist/css/bootstrap.min.css';



const App = () => (
        <AuthProvider>
            <Router>  
                <div style={{ backgroundColor: '#f4f4f2', minHeight: '100vh' }}>
                    <Layout>
                        <AppRouter />
                    </Layout>
                </div>
            </Router>
        </AuthProvider>
);



export default App;