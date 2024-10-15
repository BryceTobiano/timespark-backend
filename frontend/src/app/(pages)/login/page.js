import styles from './login.module.css';

export default function Login() {
    return (
        <div className={styles.loginContainer}>
            <div className={styles.loginCard}>
                <img src="/img/logo.png" alt="Time Spark Logo" />
                <h1>TIME SPARK</h1>
                <form>
                    <div className="form-group position-relative">
                        <input type="email" className={`form-control ${styles.formControl}`} placeholder="Email" />
                    </div>
                    <div className="form-group position-relative">
                        <span className={styles.formControlIcon}>
                            <i className="fas fa-lock"></i>
                        </span>
                        <input type="password" className={`form-control ${styles.formControl}`} placeholder="Password" />
                    </div>
                    <a href="#" className={styles.forgotPassword}>Forgot Password?</a>
                    <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
                </form>

                <div className={styles.orDivider}>
                    <span>OR</span>
                </div>

                <button className={`btn btn-light btn-block ${styles.socialBtn}`}>
                    <img src="https://img.icons8.com/color/48/000000/google-logo.png" alt="Google Logo" /> Sign in with Google
                </button>
                <button className={`btn btn-light btn-block ${styles.socialBtn}`}>
                    <img src="https://img.icons8.com/ios-filled/50/000000/mac-os.png" alt="Apple Logo" /> Sign in with Apple
                </button>
            </div>
        </div>
    );
}
