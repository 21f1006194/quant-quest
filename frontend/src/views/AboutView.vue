<template>
  <div class="about-container">
    <div class="content-wrapper">
      <div class="header-section text-center">
        <h1 class="main-title">About Us</h1>
      </div>

      <div class="about-section card">
        <div class="about-content">
          <div class="logo-container">
            <img src="@/assets/logos/Quantix_logo.jpg" alt="Quantix Logo" class="quantix-logo">
          </div>
          <div class="text-content">
            <p class="description">
              <strong>Quantix</strong> is the premier student-run club at IIT Madras, dedicated to nurturing excellence in quantitative finance. We bring together brilliant minds passionate about mathematics, finance, and technology.
            </p>
            <p class="description">
              Our mission is to create a vibrant community of quantitative thinkers and developers. Through workshops, events, and collaborative projects, we explore the fascinating intersection of data science, financial markets, and algorithmic trading.
            </p>
          </div>
        </div>
      </div>

      <div class="about-section card">
        <h2 class="section-title">About Quant Quest</h2>
        <p class="description">
          <strong>Quant Quest</strong> stands as our flagship event, meticulously crafted by the talented members of the Quantix Club. This unique competition challenges participants to apply mathematical concepts in a dynamic gaming environment.
        </p>
        <p class="description">
          Far from traditional gambling, Quant Quest is a test of analytical prowess and strategic thinking. Participants must leverage their understanding of probability theory and statistical analysis to develop winning strategies through code. It's not about chance; it's about <strong>mathematical mastery and algorithmic precision</strong>.
        </p>
      </div>

      <div class="contact-section card">
        <h2 class="section-title">Contact Us</h2>
        <div class="contact-grid">
          <div class="contact-card">
            <h3 class="contact-title">Event Head</h3>
            <p class="contact-name">Jishnu Jayaprakash</p>
            <a href="mailto:21f1006194@ds.study.iitm.ac.in" class="contact-email">21f1006194@ds.study.iitm.ac.in</a>
          </div>
          <div class="contact-card">
            <h3 class="contact-title">Event Deputy Head</h3>
            <p class="contact-name">Prasidha R</p>
            <a href="mailto:23f2005514@ds.study.iitm.ac.in" class="contact-email">23f2005514@ds.study.iitm.ac.in</a>
          </div>
          <div class="contact-card">
            <h3 class="contact-title">Quantix Club Head</h3>
            <p class="contact-name">Jeevesh Banchor</p>
            <a href="mailto:22f1000492@ds.study.iitm.ac.in" class="contact-email">22f1000492@ds.study.iitm.ac.in</a>
          </div>
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="footer-content">
        <div class="social-links">
          <a href="https://www.linkedin.com/company/quantix-the-quant-and-consulting-club-iitm-bs/" target="_blank" rel="noopener noreferrer" class="social-link">
            <i class="bi bi-linkedin"></i>
            <span>LinkedIn</span>
          </a>
          <a href="https://www.instagram.com/quantix_iitm" target="_blank" rel="noopener noreferrer" class="social-link">
            <i class="bi bi-instagram"></i>
            <span>Instagram</span>
          </a>
        </div>
        <div class="footer-text">
          <p>© 2024 Quantix Club, IIT Madras. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Component logic can be added here if needed
</script>

<style scoped>
.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
  min-height: 100vh;
  color: var(--text-light);
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  padding: var(--spacing-lg);
  flex: 1;
}

.header-section {
  margin-bottom: var(--spacing-xl);
}

.main-title {
  font-size: 3rem;
  color: var(--primary-color);
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
}

.about-section {
  margin-bottom: var(--spacing-xl);
  background-color: var(--card-dark);
  padding: var(--spacing-lg);
}

.about-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
}

.logo-container {
  flex: 0 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.quantix-logo {
  width: 250px;
  height: 250px;
  object-fit: contain;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-normal);
}

.text-content {
  flex: 1;
}

.quantix-logo:hover {
  transform: scale(1.05);
}

.section-title {
  color: var(--primary-color);
  margin-bottom: var(--spacing-md);
  font-size: 2rem;
}

.description {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: var(--spacing-md);
  color: var(--text-light);
}

.contact-section {
  margin-bottom: var(--spacing-xl);
  background-color: var(--card-dark);
  padding: var(--spacing-lg);
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-md);
}

.contact-card {
  background-color: rgba(100, 255, 218, 0.05);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  transition: transform var(--transition-normal);
}

.contact-card:hover {
  transform: translateY(-5px);
}

.contact-title {
  color: var(--primary-color);
  font-size: 1.2rem;
  margin-bottom: var(--spacing-xs);
}

.contact-name {
  color: var(--text-light);
  font-size: 1.1rem;
  margin-bottom: var(--spacing-xs);
}

.contact-email {
  color: var(--secondary-color);
  text-decoration: none;
  transition: color var(--transition-normal);
}

.contact-email:hover {
  color: var(--primary-color);
}

.social-section {
  background-color: var(--card-dark);
}

.social-links {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-md);
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: rgba(100, 255, 218, 0.1);
  border-radius: var(--border-radius-sm);
  color: var(--primary-color);
  text-decoration: none;
  transition: all var(--transition-normal);
}

.social-link:hover {
  background-color: rgba(100, 255, 218, 0.2);
  transform: translateY(-2px);
}

.social-link i {
  font-size: 1.4rem;
}

.footer {
  background-color: var(--card-dark);
  padding: var(--spacing-lg) 0;
  margin-top: auto;
  border-top: 1px solid rgba(100, 255, 218, 0.1);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  text-align: center;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: rgba(100, 255, 218, 0.1);
  border-radius: var(--border-radius-sm);
  color: var(--primary-color);
  text-decoration: none;
  transition: all var(--transition-normal);
}

.social-link:hover {
  background-color: rgba(100, 255, 218, 0.2);
  transform: translateY(-2px);
}

.social-link i {
  font-size: 1.4rem;
}

.footer-text {
  color: var(--secondary-color);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: var(--spacing-sm);
  }
  
  .main-title {
    font-size: 2.5rem;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
  }

  .social-links {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .about-content {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .quantix-logo {
    width: 200px;
    height: 200px;
  }
}
</style>

