#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for VC/Investor Test Application
Tests all endpoints with realistic data scenarios
"""

import requests
import json
import time
import uuid
from typing import Dict, Any
import sys

# Backend URL from environment
BACKEND_URL = "https://venture-rating.preview.emergentagent.com/api"

class VCTestAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'VC-Test-Backend-Tester/1.0'
        })
        self.test_results = []
        self.evaluation_ids = []
        self.payment_intent_ids = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details
        })
    
    def test_health_endpoints(self):
        """Test all health check endpoints"""
        print("\n=== TESTING HEALTH ENDPOINTS ===")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "status" in data:
                    self.log_test("GET /api/ (root endpoint)", True, f"Status: {data.get('status')}")
                else:
                    self.log_test("GET /api/ (root endpoint)", False, "Missing expected fields in response")
            else:
                self.log_test("GET /api/ (root endpoint)", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET /api/ (root endpoint)", False, f"Exception: {str(e)}")
        
        # Test main health endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("GET /api/health", True, f"Database: {data.get('database', 'unknown')}")
                else:
                    self.log_test("GET /api/health", False, "Health check failed or missing status")
            else:
                self.log_test("GET /api/health", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET /api/health", False, f"Exception: {str(e)}")
        
        # Test VC-test specific health endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/vc-test/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("GET /api/vc-test/health", True, f"Service: {data.get('service', 'vc-test')}")
                else:
                    self.log_test("GET /api/vc-test/health", False, "VC-test health check failed")
            else:
                self.log_test("GET /api/vc-test/health", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("GET /api/vc-test/health", False, f"Exception: {str(e)}")
    
    def get_realistic_idea_form_data(self) -> Dict[str, Any]:
        """Generate realistic form data for idea stage startup"""
        return {
            # Team fields
            'team-size': '2-3',
            'founder-experience': 'some-experience',
            'technical-expertise': 'tech-cofounder',
            'domain-expertise': 'deep-expertise',
            'commitment-level': 'full-time',
            
            # Market fields
            'market-size-tam': '1b-10b',
            'market-size-som': '100m-500m',
            'market-growth': 'growing',
            'market-timing': 'perfect-timing',
            'customer-segment': 'Small to medium-sized e-commerce businesses struggling with inventory management and demand forecasting. These companies typically have 10-500 employees and generate $1M-50M in annual revenue. They currently use spreadsheets or basic ERP systems that lack predictive capabilities.',
            
            # Problem/Solution fields
            'problem-severity': 'significant-pain',
            'problem-frequency': 'daily',
            'current-solution': 'poor-alternatives',
            'solution-uniqueness': 'breakthrough',
            'value-proposition': 'Our AI-powered inventory optimization platform reduces stockouts by 40% and excess inventory by 30% through advanced demand forecasting. We integrate with existing e-commerce platforms and provide real-time insights that help businesses optimize their supply chain operations.',
            
            # Competitive fields
            'defensibility': ['network-effects', 'data-moats', 'switching-costs'],
            'ip-protection': 'pending-patents',
            'competitive-timeline': 'year-plus',
            
            # Business model fields
            'revenue-model': 'subscription',
            'pricing-strategy': 'Tiered SaaS pricing model: Starter ($299/month for up to 1000 SKUs), Professional ($799/month for up to 5000 SKUs), Enterprise ($1999/month for unlimited SKUs). Pricing is based on number of SKUs managed and includes all features with enterprise support.',
            'unit-economics-visibility': 'solid-projections',
            'scalability': 'high-leverage',
            
            # Validation fields
            'validation-type': ['customer-interviews', 'pilot-customers', 'pre-orders'],
            'customer-count': '11-50'
        }
    
    def get_realistic_launched_form_data(self) -> Dict[str, Any]:
        """Generate realistic form data for launched startup"""
        base_data = self.get_realistic_idea_form_data()
        
        # Add launched-specific fields
        launched_data = {
            **base_data,
            'customer-count': '101-500',
            'cac': 150,
            'ltv': 2400,
            'payback-period': 8,
            'gross-margin': 75,
            'churn-rate': 3.5,
            'mrr': '50k-100k',
            'growth-rate': 12,
            'runway': 18,
            'funding-amount': '1m-2m',
            'use-of-funds': 'Primary use of funds: 40% for engineering team expansion (hire 3 senior developers), 30% for sales and marketing (customer acquisition and market expansion), 20% for product development (new AI features and integrations), 10% for operations and working capital.'
        }
        
        return launched_data
    
    def get_session_metadata(self, fast_completion: bool = False) -> Dict[str, Any]:
        """Generate session metadata"""
        start_time = int(time.time() * 1000)
        if fast_completion:
            start_time = int(time.time() * 1000) - 60000  # 1 minute ago (too fast)
        else:
            start_time = int(time.time() * 1000) - 300000  # 5 minutes ago (normal)
        
        return {
            'user_uuid': str(uuid.uuid4()),
            'csrf_token': f'csrf_{uuid.uuid4().hex[:16]}',
            'start_time': start_time,
            'session_id': str(uuid.uuid4())
        }
    
    def test_form_validation(self):
        """Test form validation endpoint with various scenarios"""
        print("\n=== TESTING FORM VALIDATION ===")
        
        # Test 1: Valid idea form data
        try:
            payload = {
                'form_data': self.get_realistic_idea_form_data(),
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True:
                    self.log_test("Validate idea form - valid data", True, "Form validation passed")
                else:
                    self.log_test("Validate idea form - valid data", False, f"Validation failed: {data}")
            else:
                self.log_test("Validate idea form - valid data", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Validate idea form - valid data", False, f"Exception: {str(e)}")
        
        # Test 2: Valid launched form data
        try:
            payload = {
                'form_data': self.get_realistic_launched_form_data(),
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'launched'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == True:
                    self.log_test("Validate launched form - valid data", True, "Form validation passed")
                else:
                    self.log_test("Validate launched form - valid data", False, f"Validation failed: {data}")
            else:
                self.log_test("Validate launched form - valid data", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Validate launched form - valid data", False, f"Exception: {str(e)}")
        
        # Test 3: Missing required fields
        try:
            incomplete_data = {'team-size': '2-3'}  # Missing most required fields
            payload = {
                'form_data': incomplete_data,
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == False and len(data.get('validation_errors', [])) > 0:
                    self.log_test("Validate form - missing fields", True, f"Caught {len(data['validation_errors'])} validation errors")
                else:
                    self.log_test("Validate form - missing fields", False, "Should have failed validation")
            else:
                self.log_test("Validate form - missing fields", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Validate form - missing fields", False, f"Exception: {str(e)}")
        
        # Test 4: Anti-gaming detection - too fast completion
        try:
            payload = {
                'form_data': self.get_realistic_idea_form_data(),
                'session_metadata': self.get_session_metadata(fast_completion=True),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == False and len(data.get('anti_gaming_flags', [])) > 0:
                    self.log_test("Validate form - anti-gaming (fast completion)", True, f"Detected gaming: {data['anti_gaming_flags']}")
                else:
                    self.log_test("Validate form - anti-gaming (fast completion)", False, "Should have detected fast completion")
            else:
                self.log_test("Validate form - anti-gaming (fast completion)", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Validate form - anti-gaming (fast completion)", False, f"Exception: {str(e)}")
        
        # Test 5: Anti-gaming detection - honeypot field
        try:
            form_data = self.get_realistic_idea_form_data()
            form_data['_bot_field'] = 'I am a bot'  # Honeypot field
            
            payload = {
                'form_data': form_data,
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/validate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == False and 'Bot detection triggered' in str(data.get('anti_gaming_flags', [])):
                    self.log_test("Validate form - anti-gaming (honeypot)", True, "Detected bot via honeypot field")
                else:
                    self.log_test("Validate form - anti-gaming (honeypot)", False, "Should have detected honeypot field")
            else:
                self.log_test("Validate form - anti-gaming (honeypot)", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Validate form - anti-gaming (honeypot)", False, f"Exception: {str(e)}")
    
    def test_startup_evaluation(self):
        """Test startup evaluation endpoint"""
        print("\n=== TESTING STARTUP EVALUATION ===")
        
        # Test 1: Evaluate idea startup
        try:
            payload = {
                'form_data': self.get_realistic_idea_form_data(),
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/evaluate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if (data.get('success') == True and 
                    'data' in data and 
                    'evaluation_id' in data['data'] and
                    'total_score' in data['data'] and
                    'section_scores' in data['data']):
                    
                    evaluation_id = data['data']['evaluation_id']
                    self.evaluation_ids.append(evaluation_id)
                    score = data['data']['total_score']
                    
                    self.log_test("Evaluate idea startup", True, f"Score: {score}, ID: {evaluation_id[:8]}...")
                else:
                    self.log_test("Evaluate idea startup", False, f"Missing expected fields: {data}")
            else:
                self.log_test("Evaluate idea startup", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Evaluate idea startup", False, f"Exception: {str(e)}")
        
        # Test 2: Evaluate launched startup
        try:
            payload = {
                'form_data': self.get_realistic_launched_form_data(),
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'launched'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/evaluate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if (data.get('success') == True and 
                    'data' in data and 
                    'evaluation_id' in data['data'] and
                    'total_score' in data['data']):
                    
                    evaluation_id = data['data']['evaluation_id']
                    self.evaluation_ids.append(evaluation_id)
                    score = data['data']['total_score']
                    
                    self.log_test("Evaluate launched startup", True, f"Score: {score}, ID: {evaluation_id[:8]}...")
                else:
                    self.log_test("Evaluate launched startup", False, f"Missing expected fields: {data}")
            else:
                self.log_test("Evaluate launched startup", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Evaluate launched startup", False, f"Exception: {str(e)}")
        
        # Test 3: Invalid data handling
        try:
            payload = {
                'form_data': {'invalid': 'data'},
                'session_metadata': self.get_session_metadata(),
                'startup_type': 'idea'
            }
            
            response = self.session.post(f"{BACKEND_URL}/vc-test/evaluate", json=payload)
            if response.status_code == 400:
                self.log_test("Evaluate startup - invalid data", True, "Correctly rejected invalid data")
            elif response.status_code == 200:
                data = response.json()
                if data.get('success') == False:
                    self.log_test("Evaluate startup - invalid data", True, "Validation caught invalid data")
                else:
                    self.log_test("Evaluate startup - invalid data", False, "Should have rejected invalid data")
            else:
                self.log_test("Evaluate startup - invalid data", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Evaluate startup - invalid data", False, f"Exception: {str(e)}")
    
    def test_payment_integration(self):
        """Test payment integration endpoints"""
        print("\n=== TESTING PAYMENT INTEGRATION ===")
        
        # Test 1: Get Stripe configuration
        try:
            response = self.session.get(f"{BACKEND_URL}/payments/config")
            if response.status_code == 200:
                data = response.json()
                if (data.get('success') == True and 
                    'data' in data and 
                    'publishable_key' in data['data'] and
                    'amount' in data['data']):
                    
                    self.log_test("Get payment config", True, f"Amount: ${data['data']['amount']/100:.2f}")
                else:
                    self.log_test("Get payment config", False, f"Missing expected fields: {data}")
            else:
                self.log_test("Get payment config", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get payment config", False, f"Exception: {str(e)}")
        
        # Test 2: Create payment intent with valid evaluation_id
        if self.evaluation_ids:
            try:
                payload = {
                    'evaluation_id': self.evaluation_ids[0],
                    'amount': 999,
                    'currency': 'usd'
                }
                
                response = self.session.post(f"{BACKEND_URL}/payments/create-intent", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    if (data.get('success') == True and 
                        'data' in data and 
                        'client_secret' in data['data'] and
                        'payment_intent_id' in data['data']):
                        
                        payment_intent_id = data['data']['payment_intent_id']
                        self.payment_intent_ids.append(payment_intent_id)
                        
                        self.log_test("Create payment intent", True, f"Intent ID: {payment_intent_id[:20]}...")
                    else:
                        self.log_test("Create payment intent", False, f"Missing expected fields: {data}")
                else:
                    self.log_test("Create payment intent", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("Create payment intent", False, f"Exception: {str(e)}")
        else:
            self.log_test("Create payment intent", False, "No evaluation_id available from previous tests")
        
        # Test 3: Create payment intent with invalid evaluation_id
        try:
            payload = {
                'evaluation_id': 'invalid-evaluation-id',
                'amount': 999,
                'currency': 'usd'
            }
            
            response = self.session.post(f"{BACKEND_URL}/payments/create-intent", json=payload)
            if response.status_code == 404:
                self.log_test("Create payment intent - invalid ID", True, "Correctly rejected invalid evaluation_id")
            else:
                self.log_test("Create payment intent - invalid ID", False, f"Should have returned 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Create payment intent - invalid ID", False, f"Exception: {str(e)}")
    
    def test_premium_unlock(self):
        """Test premium unlock functionality"""
        print("\n=== TESTING PREMIUM UNLOCK ===")
        
        # Test 1: Unlock premium with valid payment_intent_id
        if self.evaluation_ids and self.payment_intent_ids:
            try:
                payload = {
                    'evaluation_id': self.evaluation_ids[0],
                    'stripe_payment_intent_id': self.payment_intent_ids[0]
                }
                
                response = self.session.post(f"{BACKEND_URL}/vc-test/unlock-premium", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    if (data.get('success') == True and 
                        'data' in data and 
                        'deep_analysis' in data['data'] and
                        'recommendations' in data['data']):
                        
                        analysis_length = len(data['data']['deep_analysis'])
                        self.log_test("Unlock premium analysis", True, f"Generated {analysis_length} chars of analysis")
                    else:
                        self.log_test("Unlock premium analysis", False, f"Missing expected fields: {data}")
                else:
                    self.log_test("Unlock premium analysis", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("Unlock premium analysis", False, f"Exception: {str(e)}")
        else:
            self.log_test("Unlock premium analysis", False, "No evaluation_id or payment_intent_id available")
        
        # Test 2: Invalid payment verification
        if self.evaluation_ids:
            try:
                payload = {
                    'evaluation_id': self.evaluation_ids[0],
                    'stripe_payment_intent_id': 'invalid-payment-intent-id'
                }
                
                response = self.session.post(f"{BACKEND_URL}/vc-test/unlock-premium", json=payload)
                if response.status_code == 400:
                    self.log_test("Unlock premium - invalid payment", True, "Correctly rejected invalid payment_intent_id")
                else:
                    self.log_test("Unlock premium - invalid payment", False, f"Should have returned 400, got {response.status_code}")
            except Exception as e:
                self.log_test("Unlock premium - invalid payment", False, f"Exception: {str(e)}")
        else:
            self.log_test("Unlock premium - invalid payment", False, "No evaluation_id available")
        
        # Test 3: Invalid evaluation_id
        if self.payment_intent_ids:
            try:
                payload = {
                    'evaluation_id': 'invalid-evaluation-id',
                    'stripe_payment_intent_id': self.payment_intent_ids[0]
                }
                
                response = self.session.post(f"{BACKEND_URL}/vc-test/unlock-premium", json=payload)
                if response.status_code == 404:
                    self.log_test("Unlock premium - invalid evaluation", True, "Correctly rejected invalid evaluation_id")
                else:
                    self.log_test("Unlock premium - invalid evaluation", False, f"Should have returned 404, got {response.status_code}")
            except Exception as e:
                self.log_test("Unlock premium - invalid evaluation", False, f"Exception: {str(e)}")
        else:
            self.log_test("Unlock premium - invalid evaluation", False, "No payment_intent_id available")
    
    def test_evaluation_retrieval(self):
        """Test evaluation retrieval endpoint"""
        print("\n=== TESTING EVALUATION RETRIEVAL ===")
        
        if self.evaluation_ids:
            try:
                evaluation_id = self.evaluation_ids[0]
                response = self.session.get(f"{BACKEND_URL}/vc-test/evaluation/{evaluation_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    if (data.get('success') == True and 
                        'data' in data and 
                        'total_score' in data['data']):
                        
                        self.log_test("Get evaluation by ID", True, f"Retrieved evaluation with score: {data['data']['total_score']}")
                    else:
                        self.log_test("Get evaluation by ID", False, f"Missing expected fields: {data}")
                else:
                    self.log_test("Get evaluation by ID", False, f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test("Get evaluation by ID", False, f"Exception: {str(e)}")
        else:
            self.log_test("Get evaluation by ID", False, "No evaluation_id available")
        
        # Test invalid evaluation_id
        try:
            response = self.session.get(f"{BACKEND_URL}/vc-test/evaluation/invalid-id")
            if response.status_code == 404:
                self.log_test("Get evaluation - invalid ID", True, "Correctly returned 404 for invalid ID")
            else:
                self.log_test("Get evaluation - invalid ID", False, f"Should have returned 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Get evaluation - invalid ID", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive VC Test Backend API Testing")
        print(f"Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        self.test_health_endpoints()
        self.test_form_validation()
        self.test_startup_evaluation()
        self.test_payment_integration()
        self.test_premium_unlock()
        self.test_evaluation_retrieval()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print(f"\n🎯 Generated {len(self.evaluation_ids)} evaluation(s) and {len(self.payment_intent_ids)} payment intent(s)")
        
        return passed == total

if __name__ == "__main__":
    tester = VCTestAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend API is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the details above.")
        sys.exit(1)