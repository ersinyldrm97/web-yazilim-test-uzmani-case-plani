from locust import HttpUser, task, between

class BaykarWebsiteUser(HttpUser):
  wait_time = between(1, 3)
  
  @task
  def view_homepage(self):
      self.client.get("/")

  @task
  def view_career_page(self):
      self.client.get("basvuru/acik-pozisyonlar/")

  @task
  def search_positions(self):
    payload = {"keyword": "Ana Veri Personeli"}
    headers= {"Content-Type": "application/json"}
    self.client.post("/tr/basvuru/acik-pozisyonlar/#program=34,24,22", json=payload, headers=headers)