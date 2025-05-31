import {Outlet} from "react-router-dom";
import Header from "../sections/Header";
import Nav from "../sections/Nav";
import Footer from "../sections/Footer";

function MainLayout() {
    return (
        <div className="min-h-screen flex flex-col">
          <Header />
          <Nav />
          <main className="flex-grow">
            <Outlet />
          </main>
          <Footer />
        </div>
  );
}

export default MainLayout