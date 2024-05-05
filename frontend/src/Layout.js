import Nav from './Nav';
import Container from 'react-bootstrap/Container';

const Layout = ({ children }) => {
    return (
        <>
            <Nav />

            <Container>
                
                {children}
            </Container>
        </>
    );
}

export default Layout;