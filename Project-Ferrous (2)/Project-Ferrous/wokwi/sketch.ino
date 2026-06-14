/*
 * Project Ferrous — Tier 3 Bare-Metal Field HUD (Ultimate Demo Version)
 * OT-Quest | Joshua Brunner | Class A Water Treatment Operator
 *
 * Hardware: ESP32-2432S028R (Cheap Yellow Display)
 * Driver Stack: Adafruit_GFX + Adafruit_ILI9341
 *
 * TOGGLE: Set RUN_BENCH_SIMULATION true for demo/Wokwi
 *         Set false for live GPS + Shodan field deployment
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPSPlus.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <ArduinoJson.h>

// ─── CONFIGURATION ────────────────────────────────────────────────────────────
const char* ssid      = "FieldHotspot";
const char* password  = "OperationalKey";
const char* shodanKey = "YOUR_SHODAN_API_KEY"; // Requires Shodan Membership ~$69

// ──────────────────────────────────────────────────────────────────────────────
// [TOGGLE SWITCH]
// true  = Simulation mode — mock threat data, no API calls, safe for demo
// false = Live mode — real GPS hardware + live Shodan queries
#define RUN_BENCH_SIMULATION true
// ──────────────────────────────────────────────────────────────────────────────

// CYD Pin Layout (Wokwi verified)
#define TFT_MISO 12
#define TFT_MOSI 13
#define TFT_CLK  14
#define TFT_CS   15
#define TFT_DC   2
#define TFT_RST  4

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_MOSI, TFT_CLK, TFT_RST, TFT_MISO);
TinyGPSPlus gps;

// Onboard RGB LED (Active LOW on CYD)
#define LED_RED   4
#define LED_GREEN 16
#define LED_BLUE  17

// Timing gates
unsigned long lastQueryTime  = 0;
unsigned long lastWifiCheck  = 0;
const unsigned long queryInterval = 20000;

bool lastWifiStatus    = false;
int  lastExposureCount = -1;

// ─── MOCK GPS ROUTE ───────────────────────────────────────────────────────────
int mockRouteIndex = 0;
const int totalMockPoints = 4;

struct MockCoordinate {
  double      latitude;
  double      longitude;
  const char* locationName;
};

MockCoordinate mockRoute[totalMockPoints] = {
  {30.6150, -97.6600, "Booster Station 1"},
  {30.6123, -97.6543, "Primary Plant Intake"},
  {30.6200, -97.6700, "Elevated Storage Tank"},
  {30.6500, -97.7000, "Clear Perimeter Zone"}
};

// ─── MOCK THREAT DATABASE ─────────────────────────────────────────────────────
// Mirrors the Python ferrous_full.py mock data layer.
// In live mode this is replaced by real Shodan API responses.
// Coordinates must match mockRoute entries to 4 decimal places.

struct MockMatch {
  const char* ip;
  int         port;
  const char* org;
  const char* city;
  const char* banner;
};

struct MockThreatEntry {
  double      lat;
  double      lon;
  int         total;
  MockMatch   matches[3];
  int         matchCount;
};

MockThreatEntry mockDB[] = {

  // Checkpoint 1 — Booster Station
  { 30.6150, -97.6600, 1, {
    { "192.168.42.11", 502,
      "Municipal Water District",
      "Booster Station 1",
      "Modbus TCP | Func: 01,02,03,04,05,06 | Schneider Quantum PLC" }
  }, 1 },

  // Checkpoint 2 — Water Plant (two exposures)
  { 30.6123, -97.6543, 2, {
    { "10.240.12.5", 102,
      "City Utility Grid Operations",
      "Water Plant Primary Intake",
      "Siemens S7 ISO-on-TCP | CPU S7-300 v3.2.1 | CVE-2022-38773 CVSS 9.8 ACTIVE EXPLOIT" },
    { "10.240.12.6", 1911,
      "City Utility Grid Operations",
      "Water Plant High Service Pumps",
      "Tridium Niagara Fox v4.10.0.154 | Auth: UNENCRYPTED CLEARTEXT" }
  }, 2 },

  // Checkpoint 3 — Elevated Tank
  { 30.6200, -97.6700, 1, {
    { "172.16.89.4", 47808,
      "County Water Infrastructure",
      "Elevated Storage Tank Telemetry",
      "BACnet/IP | Delta Controls | Object: Tank_Level_Transmitter" }
  }, 1 },

  // Checkpoint 4 — Clear perimeter
  { 30.6500, -97.7000, 0, {}, 0 }
};

const int mockDBSize = 4;

// ─── MOCK LOOKUP ──────────────────────────────────────────────────────────────
// Returns pointer to matching MockThreatEntry or nullptr if no match
MockThreatEntry* lookupMockThreat(double lat, double lon) {
  for (int i = 0; i < mockDBSize; i++) {
    if (abs(mockDB[i].lat - lat) < 0.0005 &&
        abs(mockDB[i].lon - lon) < 0.0005) {
      return &mockDB[i];
    }
  }
  return nullptr;
}

// ─── SETUP ────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial2.begin(9600);

  pinMode(LED_RED,   OUTPUT); digitalWrite(LED_RED,   HIGH);
  pinMode(LED_GREEN, OUTPUT); digitalWrite(LED_GREEN, HIGH);
  pinMode(LED_BLUE,  OUTPUT); digitalWrite(LED_BLUE,  HIGH);

  tft.begin();
  tft.setRotation(3);
  renderClearHUD();

  WiFi.begin(ssid, password);

  if (RUN_BENCH_SIMULATION) {
    Serial.println("[RUN CONFIG] SIMULATION MODE ACTIVE");
    Serial.println("[RUN CONFIG] Type a coordinate (e.g. 30.6123,-97.6543) to trigger mock threat lookup.");
    Serial.println("[RUN CONFIG] Or wait — auto-steps through mock route every 20s.");
  } else {
    Serial.println("[RUN CONFIG] LIVE FIELD MODE ACTIVE — GPS + Shodan armed.");
  }
}

// ─── MAIN LOOP ────────────────────────────────────────────────────────────────
void loop() {
  unsigned long now = millis();

  // 1. Always listen for manual serial input
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() > 0) {
      if (input.startsWith("$")) {
        // NMEA sentence
        for (unsigned int i = 0; i < input.length(); i++) gps.encode(input[i]);
        if (gps.location.isUpdated()) {
          updateHUDCoordinates(gps.location.lat(), gps.location.lng(), "MANUAL NMEA");
          executeQuery(gps.location.lat(), gps.location.lng());
          lastQueryTime = now;
        }
      } else if (input.indexOf(',') != -1) {
        // Raw lat,lon
        int comma = input.indexOf(',');
        double mLat = input.substring(0, comma).toDouble();
        double mLon = input.substring(comma + 1).toDouble();
        if (mLat != 0.0 && mLon != 0.0) {
          Serial.printf("[INPUT] Manual coordinate: %.4f, %.4f\n", mLat, mLon);
          updateHUDCoordinates(mLat, mLon, "MANUAL INPUT");
          executeQuery(mLat, mLon);
          lastQueryTime = now;
        }
      }
    }
  }

  // 2. Auto-step simulation route OR read live GPS
  if (now - lastQueryTime >= queryInterval || lastQueryTime == 0) {
    if (RUN_BENCH_SIMULATION) {
      double sLat = mockRoute[mockRouteIndex].latitude;
      double sLon = mockRoute[mockRouteIndex].longitude;
      Serial.printf("[SIMULATOR] Auto-stepping: %s (%.4f, %.4f)\n",
                    mockRoute[mockRouteIndex].locationName, sLat, sLon);
      updateHUDCoordinates(sLat, sLon, mockRoute[mockRouteIndex].locationName);
      executeQuery(sLat, sLon);
      mockRouteIndex = (mockRouteIndex + 1) % totalMockPoints;
    } else {
      while (Serial2.available() > 0) gps.encode(Serial2.read());
      if (gps.location.isUpdated()) {
        updateHUDCoordinates(gps.location.lat(), gps.location.lng(), "HARDWARE GPS");
        executeQuery(gps.location.lat(), gps.location.lng());
      }
    }
    lastQueryTime = now;
  }

  // 3. WiFi status check
  if (now - lastWifiCheck >= 5000) {
    lastWifiCheck = now;
    bool connected = (WiFi.status() == WL_CONNECTED);
    if (connected != lastWifiStatus) {
      updateNetworkHUD(connected);
      lastWifiStatus = connected;
    }
  }
}

// ─── QUERY ROUTER ─────────────────────────────────────────────────────────────
// Routes to mock lookup or live Shodan depending on toggle
void executeQuery(double lat, double lon) {
  if (RUN_BENCH_SIMULATION) {
    executeMockQuery(lat, lon);
  } else {
    executeLiveQuery(lat, lon);
  }
}

// ─── MOCK QUERY ENGINE ────────────────────────────────────────────────────────
void executeMockQuery(double lat, double lon) {
  Serial.printf("[SIMULATOR] Mock threat lookup: %.4f, %.4f\n", lat, lon);
  delay(800); // Simulate API latency

  MockThreatEntry* entry = lookupMockThreat(lat, lon);

  tft.fillRect(10, 110, 300, 120, ILI9341_BLACK);
  tft.setCursor(10, 110);

  if (entry == nullptr || entry->total == 0) {
    digitalWrite(LED_RED,   HIGH);
    digitalWrite(LED_GREEN, LOW);
    tft.setTextSize(2);
    tft.setTextColor(ILI9341_GREEN);
    tft.println("PERIMETER: SECURE");
    tft.setTextSize(1);
    tft.setCursor(10, 135);
    tft.setTextColor(ILI9341_CYAN);
    tft.println("No OT exposure indexed in this grid cell.");
    Serial.println("[SIMULATOR] Area clear — no mock threats at this coordinate.");
    return;
  }

  // Exposure found
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED,   LOW);
  tft.setTextSize(2);
  tft.setTextColor(ILI9341_RED);
  tft.printf("EXPOSURE: %d VECTOR", entry->total);
  if (entry->total > 1) tft.print("S");
  tft.println();

  tft.setTextSize(1);
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(10, 135);

  for (int i = 0; i < entry->matchCount && i < 3; i++) {
    MockMatch& m = entry->matches[i];
    tft.printf("IP:  %s:%d\n", m.ip, m.port);
    tft.printf("Org: %s\n", m.org);
    tft.printf("%s\n\n", m.banner);
    Serial.printf("[SIMULATOR] Match: %s:%d | %s\n", m.ip, m.port, m.banner);
  }
}

// ─── LIVE QUERY ENGINE ────────────────────────────────────────────────────────
void executeLiveQuery(double lat, double lon) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[LIVE] Query bypassed — no network uplink.");
    return;
  }

  digitalWrite(LED_BLUE, LOW);
  HTTPClient http;

  String url = "https://api.shodan.io/shodan/host/search?key=" + String(shodanKey) +
               "&query=geo:" + String(lat, 4) + "," + String(lon, 4) + ",1" +
               " port:502,47808,1911,20000,102";

  Serial.println("[LIVE] Shodan query: " + url);
  http.begin(url);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    DynamicJsonDocument doc(16384);
    DeserializationError err = deserializeJson(doc, payload);
    if (err) { Serial.printf("[ERROR] JSON parse failed: %s\n", err.c_str()); return; }

    int total = doc["total"] | 0;
    tft.fillRect(10, 110, 300, 120, ILI9341_BLACK);
    tft.setCursor(10, 110);

    if (total > 0) {
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(LED_RED,   LOW);
      tft.setTextSize(2);
      tft.setTextColor(ILI9341_RED);
      tft.printf("EXPOSURE: %d VECTORS\n", total);
      tft.setTextSize(1);
      tft.setTextColor(ILI9341_WHITE);
      tft.setCursor(10, 135);

      JsonArray matches = doc["matches"].as<JsonArray>();
      int count = 0;
      for (JsonObject match : matches) {
        if (count++ >= 3) break;
        tft.printf("IP:  %s:%d\n", match["ip_str"].as<const char*>(), match["port"].as<int>());
        tft.printf("Org: %s\n\n", match["org"] | "Unknown");
      }
    } else {
      digitalWrite(LED_RED,   HIGH);
      digitalWrite(LED_GREEN, LOW);
      tft.setTextSize(2);
      tft.setTextColor(ILI9341_GREEN);
      tft.println("PERIMETER: SECURE");
    }
  } else {
    Serial.printf("[LIVE] Shodan HTTP error: %d\n", httpCode);
  }

  http.end();
  digitalWrite(LED_BLUE, HIGH);
}

// ─── HUD HELPERS ──────────────────────────────────────────────────────────────
void renderClearHUD() {
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(2);
  tft.setCursor(10, 10);
  tft.println("FERROUS FIELD HUD");
  tft.drawFastHLine(10, 32, 300, ILI9341_GREEN);
  tft.setTextSize(1);
  tft.setCursor(10, 75);
  tft.setTextColor(ILI9341_CYAN);
  tft.println("Awaiting telemetry initialization...");
}

void updateHUDCoordinates(double lat, double lon, const char* label) {
  tft.fillRect(10, 60, 300, 40, ILI9341_BLACK);
  tft.setTextSize(1);
  tft.setTextColor(ILI9341_CYAN);
  tft.setCursor(10, 60);
  tft.printf("MODE: %s\n", label);
  tft.printf("LAT: %.4f  |  LON: %.4f\n", lat, lon);
}

void updateNetworkHUD(bool connected) {
  tft.fillRect(10, 45, 300, 12, ILI9341_BLACK);
  tft.setCursor(10, 45);
  tft.setTextSize(1);
  if (connected) {
    tft.setTextColor(ILI9341_GREEN);
    tft.printf("UPLINK: CONNECTED | %s", WiFi.localIP().toString().c_str());
    digitalWrite(LED_BLUE, HIGH);
  } else {
    tft.setTextColor(ILI9341_RED);
    tft.println("UPLINK: OFFLINE (DEMO/FIELD MODE)");
    digitalWrite(LED_BLUE, LOW);
  }
}
