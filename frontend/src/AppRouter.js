import { Route, Routes, Navigate} from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './utils/ProtectedRoute';
import LoginForm from './auth/LoginForm';
import StudentProfile from './components/StudentProfile';
import JobPostForm from './forms/JobPostForm';
import JobBrowser from './components/JobBrowser';
import JobPostDetail from './components/JobPostDetail';
import ApplicationDetail from './components/ApplicationDetail';
import StudentAppointments from './components/StudentAppointments';
import StudentEvents from './components/StudentEvents';
import AppointmentDetail from './components/AppointmentDetail';
import EventBrowser from './components/EventBrowser';
import EventDetail from './components/EventDetail';
import StudentInteractions from './components/StudentInteractions';
import StudentApplications from './components/StudentApplications';
import StudentDegrees from './components/StudentDegrees';
import StudentBrowser from './components/StudentBrowser';
import StaffProfile from './components/StaffProfile';
import StudentActivities from './components/StudentActivities';
import AppointmentBrowser from './components/AppointmentBrowser';
import StaffBrowser from './components/StaffBrowser';
import StaffAppointments from './components/StaffAppointments';
import UpcomingApplicationActivities from './components/UpcomingApplicationActivities';
import StaffInteractions from './components/StaffInteractions';
import Logout from './auth/Logout';
import StudentProfileRoutes from './components/StudentProfileRoutes';
import StaffProfileRoutes from './components/StaffProfileRoutes';

const AppRouter = () => {
    const { isAuthenticated, userType, loading } = useAuth();


    if (loading) {
        return <h1>Loading...</h1>
    }

    function profilePage() {
        if (userType === 'student') {
            return "/students/me"
        } else if (userType === 'staff') {
            return "/staff/me"
        }
    }

    const profileEndpoint = profilePage();

    return (
        <Routes>

            <Route path="/" element={!isAuthenticated ? <Navigate to="/login" />: <Navigate to={`${profileEndpoint}`} />} />
            <Route path="*" element={<Navigate to={`${profileEndpoint}`} />} />
            <Route path="/login" element={!isAuthenticated ? <LoginForm />: <Navigate to="/" />} />
            <Route path="/logout" element={<Logout />} />
            {/* Routes for jobs and related tasks (creation, application, activities */}
            <Route path="/job-posts" element={<ProtectedRoute allowedUserTypes={['student', 'staff']}>
                    <JobBrowser />
                </ProtectedRoute>
            }/>

            <Route path="/job-posts/create-job" element={
                <ProtectedRoute allowedUserTypes={['staff', 'company']}>
                    <JobPostForm />
                </ProtectedRoute>
            }/>

            <Route path="/job-posts/:id" element={<ProtectedRoute>
                    <JobPostDetail />
                </ProtectedRoute>
            }/>

            <Route path="/applications/:id" element={<ProtectedRoute>
                    <ApplicationDetail />
                </ProtectedRoute>
            }/>


            {/* Routes for viewing appointments */}
            <Route path="/appointments/:id" element={<ProtectedRoute>
                    <AppointmentDetail />
                </ProtectedRoute>
            }/>

            {/* Routes for viewing events*/}
            <Route path="/events/:id" element={<ProtectedRoute>
                    <EventDetail />
                </ProtectedRoute>
            }/>

            

            {/* Routes for students to view their own info and browse info*/}
            <Route path="/students/me/degrees" element={<ProtectedRoute allowedUserTypes={['student']}>
                <StudentDegrees />
            </ProtectedRoute>
            }/>

            

            <Route path="/appointments" element={<ProtectedRoute allowedUserTypes={['student']}>
                    <AppointmentBrowser />
                </ProtectedRoute>
            }/>

            <Route path="/events" element={<ProtectedRoute allowedUserTypes={['student']}>
                    <EventBrowser />
                </ProtectedRoute>
            }/>


            {/* Routes for staff to view their own info */}
            <Route path="/staff" element={<ProtectedRoute allowedUserTypes={['student', 'staff']}>
                <StaffBrowser />
            </ProtectedRoute>
            }/>




            {/* Routes for staff to view students */}
            <Route path="/students" element={<ProtectedRoute allowedUserTypes={['staff']}>
                <StudentBrowser />
            </ProtectedRoute>
            }/>

            <Route path="/applications/activities" element={<ProtectedRoute allowedUserTypes={['staff']}>
                <UpcomingApplicationActivities />
            </ProtectedRoute>
            }/>

     

            
            {/* New setup for more of a SPA feel for the web app */}
            {/* Student Profile Routes */}
            <Route path="/students/me/*" element={<ProtectedRoute allowedUserTypes={['student']}>
                <StudentProfileRoutes isCurrentUser={true} />
            </ProtectedRoute>
            }>
                <Route index element={<Navigate to="about" replace />} />
                <Route path="about" element={<StudentProfile />} />
                <Route path="applications" element={<StudentApplications />} />
                <Route path="activities" element={<StudentActivities />} />
                <Route path="interactions" element={<StudentInteractions />} />
                <Route path="appointments" element={<StudentAppointments />} />
                <Route path="events" element={<StudentEvents />} />
            </Route>


            <Route path="/students/:id/*" element={<ProtectedRoute allowedUserTypes={['staff']}>
                <StudentProfileRoutes isCurrentUser={false} />
            </ProtectedRoute>
            }>
                <Route index element={<Navigate to="about" replace />} />
                <Route path="about" element={<StudentProfile />} />
                <Route path="applications" element={<StudentApplications />} />
                <Route path="activities" element={<StudentActivities />} />
                <Route path="interactions" element={<StudentInteractions />} />
                <Route path="appointments" element={<StudentAppointments />} />
                <Route path="events" element={<StudentEvents />} />
            </Route>

            
            {/* Staff Profile Routes */}
            <Route path="/staff/me/*" element={<ProtectedRoute allowedUserTypes={['staff']}>
                <StaffProfileRoutes  isCurrentUser={true}/>
            </ProtectedRoute>
            }>
                <Route index element={<Navigate to="about" replace />} />
                <Route path="about" element={<StaffProfile />} />
                <Route path="appointments" element={<StaffAppointments />} />
                <Route path="interactions" element={<StaffInteractions />} />
            </Route>

            <Route path="/staff/:id/*" element={<ProtectedRoute allowedUserTypes={['student']}>
                <StaffProfileRoutes isCurrentUser={false}/>
            </ProtectedRoute>
            }>
                <Route index element={<Navigate to="about" replace />} />
                <Route path="about" element={<StaffProfile />} />
                <Route path="appointments" element={<StaffAppointments />} />
            </Route>
            

            
        </Routes>
    );
};

export default AppRouter;