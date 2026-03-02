// Google Apps Script - Admin Panel Backend for 2030 Intelligence Report
// ES5 compatible - no arrow functions, const/let, template literals, etc.

var SHEET_NAME_CONFIG = 'Config';
var SHEET_NAME_ADMINS = 'Admins';
var SHEET_NAME_ADVISORS = 'Advisors';
var SHEET_NAME_FEEDBACK = 'Feedback';
var SHEET_NAME_ACTIONS = 'ActionItems';
var SHEET_NAME_ANALYTICS_DAILY = 'Analytics_Daily';
var SHEET_NAME_CONTENT_PERF = 'ContentPerformance';
var SHEET_NAME_EMAIL_REPORTS = 'EmailReports';

var JWT_SECRET = 'JWT_SECRET';
var OTP_EXPIRY_MINUTES = 15;
var TOKEN_EXPIRY_HOURS = 8;
var ALLOWED_ORIGIN = '*';

// ============================================================================
// MAIN ENTRY POINTS
// ============================================================================

function doPost(e) {
  try {
    var response = handleRequest(e);
    return buildJsonResponse(response);
  } catch (error) {
    return buildJsonResponse({
      success: false,
      error: error.toString()
    });
  }
}

function doGet(e) {
  try {
    // Handle CORS preflight
    if (e.parameter.action === 'ping') {
      return buildJsonResponse({ success: true, message: 'pong' });
    }

    var response = handleRequest(e);
    return buildJsonResponse(response);
  } catch (error) {
    return buildJsonResponse({
      success: false,
      error: error.toString()
    });
  }
}

// ============================================================================
// REQUEST ROUTER
// ============================================================================

function handleRequest(e) {
  var action = e.parameter.action || '';
  var contentBody = e.postData ? e.postData.contents : '';
  var data = {};

  try {
    if (contentBody) {
      data = JSON.parse(contentBody);
    }
  } catch (parseError) {
    return { success: false, error: 'Invalid JSON in request body' };
  }

  // Initialize sheet on first run
  initializeSheet();

  // Route to appropriate handler
  switch (action) {
    // Authentication
    case 'request_otp':
      return handleRequestOtp(data);
    case 'verify_otp':
      return handleVerifyOtp(data);
    case 'validate_token':
      return handleValidateToken(data);

    // Feedback
    case 'submit_feedback':
      return handleSubmitFeedback(data);
    case 'list_feedback':
      return handleListFeedback(data);
    case 'update_feedback':
      return handleUpdateFeedback(data);
    case 'bulk_update_feedback':
      return handleBulkUpdateFeedback(data);

    // Admin Management
    case 'list_admins':
      return handleListAdmins(data);
    case 'add_admin':
      return handleAddAdmin(data);
    case 'remove_admin':
      return handleRemoveAdmin(data);

    // Advisor Management
    case 'list_advisors':
      return handleListAdvisors(data);
    case 'add_advisor':
      return handleAddAdvisor(data);
    case 'remove_advisor':
      return handleRemoveAdvisor(data);

    // Action Items
    case 'list_actions':
      return handleListActions(data);
    case 'create_action':
      return handleCreateAction(data);
    case 'update_action':
      return handleUpdateAction(data);

    // Analytics
    case 'get_analytics':
      return handleGetAnalytics(data);
    case 'get_performance':
      return handleGetPerformance(data);

    // Dashboard
    case 'get_dashboard':
      return handleGetDashboard(data);

    default:
      return { success: false, error: 'Unknown action: ' + action };
  }
}

// ============================================================================
// AUTHENTICATION HANDLERS
// ============================================================================

function handleRequestOtp(data) {
  var email = data.email || '';

  if (!email || !isValidEmail(email)) {
    return { success: false, error: 'Invalid email address' };
  }

  // Check if email exists in Admins sheet
  var admins = getSheetData(SHEET_NAME_ADMINS);
  var adminExists = false;
  for (var i = 0; i < admins.length; i++) {
    if (admins[i][1] === email && admins[i][5] !== 'inactive') {
      adminExists = true;
      break;
    }
  }

  if (!adminExists) {
    return { success: false, error: 'Email not found in admin list' };
  }

  // Generate 6-digit OTP
  var otp = String(Math.floor(Math.random() * 1000000));
  while (otp.length < 6) {
    otp = '0' + otp;
  }

  // Store OTP with expiry
  var now = new Date();
  var expiryTime = new Date(now.getTime() + OTP_EXPIRY_MINUTES * 60000);

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var adminRow = -1;
  var data = sheet.getDataRange().getValues();

  for (var i = 1; i < data.length; i++) {
    if (data[i][1] === email) {
      adminRow = i + 1;
      sheet.getRange(adminRow, 6).setValue(otp);
      sheet.getRange(adminRow, 7).setValue(expiryTime);
      break;
    }
  }

  // Send OTP email
  var subject = 'Your 2030 Intelligence Report Admin Login Code';
  var htmlBody = getOtpEmailTemplate(otp, email);

  try {
    GmailApp.sendEmail(email, subject, '', {
      htmlBody: htmlBody
    });
  } catch (e) {
    return { success: false, error: 'Failed to send email: ' + e };
  }

  return {
    success: true,
    message: 'OTP sent to ' + email
  };
}

function handleVerifyOtp(data) {
  var email = data.email || '';
  var otp = data.otp || '';

  if (!email || !otp) {
    return { success: false, error: 'Missing email or OTP' };
  }

  // Find admin and verify OTP
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();
  var adminData = null;
  var adminRow = -1;

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] === email) {
      adminRow = i + 1;
      adminData = allData[i];
      break;
    }
  }

  if (!adminData) {
    return { success: false, error: 'Admin not found' };
  }

  var storedOtp = adminData[5];
  var expiryTime = new Date(adminData[6]);
  var now = new Date();

  if (storedOtp !== otp) {
    return { success: false, error: 'Invalid OTP' };
  }

  if (now > expiryTime) {
    return { success: false, error: 'OTP expired' };
  }

  // Clear OTP and generate token
  sheet.getRange(adminRow, 6).clearContent();
  sheet.getRange(adminRow, 7).clearContent();

  // Update last_login
  sheet.getRange(adminRow, 8).setValue(now);

  // Generate token
  var token = generateToken(email);

  // Return admin data (without sensitive fields)
  var adminDataObj = {
    admin_id: adminData[0],
    email: adminData[1],
    name: adminData[2],
    role: adminData[3],
    status: adminData[4]
  };

  return {
    success: true,
    token: token,
    admin_data: adminDataObj
  };
}

function handleValidateToken(data) {
  var token = data.token || '';

  if (!token) {
    return { success: false, valid: false, error: 'Missing token' };
  }

  var validated = validateToken(token);

  if (!validated) {
    return { success: false, valid: false, error: 'Invalid or expired token' };
  }

  // Decode token to get email
  var email = decodeTokenEmail(token);

  // Get admin data
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] === email) {
      return {
        success: true,
        valid: true,
        admin_data: {
          admin_id: allData[i][0],
          email: allData[i][1],
          name: allData[i][2],
          role: allData[i][3],
          status: allData[i][4]
        }
      };
    }
  }

  return { success: false, valid: false, error: 'Admin not found' };
}

// ============================================================================
// FEEDBACK HANDLERS
// ============================================================================

function handleSubmitFeedback(data) {
  var pageUrl = data.page_url || '';
  var feedbackType = data.feedback_type || '';
  var message = data.message || '';
  var userEmail = data.user_email || '';

  if (!message || !feedbackType) {
    return { success: false, error: 'Missing required fields' };
  }

  // Generate feedback ID
  var feedbackId = 'FB-' + new Date().getTime();

  // Add to Feedback sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var now = new Date();

  sheet.appendRow([
    feedbackId,
    userEmail,
    pageUrl,
    feedbackType,
    message,
    'open',
    'normal',
    '',
    '',
    now,
    '',
    'new'
  ]);

  return {
    success: true,
    feedback_id: feedbackId
  };
}

function handleListFeedback(data) {
  var token = data.token || '';
  var statusFilter = data.status_filter || '';
  var limit = data.limit || 50;
  var offset = data.offset || 0;

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var allData = sheet.getDataRange().getValues();

  var filtered = [];
  for (var i = 1; i < allData.length; i++) {
    var status = allData[i][5];

    if (statusFilter && status !== statusFilter) {
      continue;
    }

    filtered.push({
      feedback_id: allData[i][0],
      user_email: allData[i][1],
      page_url: allData[i][2],
      feedback_type: allData[i][3],
      message: allData[i][4],
      status: allData[i][5],
      priority: allData[i][6],
      assigned_to: allData[i][7],
      reply: allData[i][8],
      created_at: allData[i][9],
      updated_at: allData[i][10],
      flag: allData[i][11]
    });
  }

  // Sort by created_at descending
  filtered.sort(function(a, b) {
    return new Date(b.created_at) - new Date(a.created_at);
  });

  var paginated = filtered.slice(offset, offset + limit);

  return {
    success: true,
    data: paginated,
    total: filtered.length,
    offset: offset,
    limit: limit
  };
}

function handleUpdateFeedback(data) {
  var token = data.token || '';
  var feedbackId = data.feedback_id || '';
  var status = data.status || '';
  var priority = data.priority || '';
  var assignedTo = data.assigned_to || '';
  var reply = data.reply || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!feedbackId) {
    return { success: false, error: 'Missing feedback_id' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var allData = sheet.getDataRange().getValues();
  var feedbackRow = -1;
  var userEmail = '';

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][0] === feedbackId) {
      feedbackRow = i + 1;
      userEmail = allData[i][1];
      break;
    }
  }

  if (feedbackRow === -1) {
    return { success: false, error: 'Feedback not found' };
  }

  // Update fields
  if (status) {
    sheet.getRange(feedbackRow, 6).setValue(status);
  }
  if (priority) {
    sheet.getRange(feedbackRow, 7).setValue(priority);
  }
  if (assignedTo) {
    sheet.getRange(feedbackRow, 8).setValue(assignedTo);
  }
  if (reply) {
    sheet.getRange(feedbackRow, 9).setValue(reply);
  }

  sheet.getRange(feedbackRow, 11).setValue(new Date());

  // Send reply email if reply provided
  if (reply && userEmail) {
    var subject = 'Re: Your feedback on The 2030 Intelligence Report';
    var htmlBody = getFeedbackReplyEmailTemplate(reply);

    try {
      GmailApp.sendEmail(userEmail, subject, '', {
        htmlBody: htmlBody
      });
    } catch (e) {
      // Log but don't fail
    }
  }

  return { success: true };
}

function handleBulkUpdateFeedback(data) {
  var token = data.token || '';
  var feedbackIds = data.feedback_ids || [];
  var field = data.field || '';
  var value = data.value || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!field || feedbackIds.length === 0) {
    return { success: false, error: 'Missing field or feedback_ids' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var allData = sheet.getDataRange().getValues();
  var columnMap = { 'status': 6, 'priority': 7, 'assigned_to': 8 };
  var columnIndex = columnMap[field];

  if (!columnIndex) {
    return { success: false, error: 'Invalid field: ' + field };
  }

  var updateCount = 0;

  for (var i = 1; i < allData.length; i++) {
    for (var j = 0; j < feedbackIds.length; j++) {
      if (allData[i][0] === feedbackIds[j]) {
        sheet.getRange(i + 1, columnIndex).setValue(value);
        updateCount++;
      }
    }
  }

  return {
    success: true,
    count: updateCount
  };
}

// ============================================================================
// ADMIN MANAGEMENT HANDLERS
// ============================================================================

function handleListAdmins(data) {
  var token = data.token || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  // Check if requester is owner
  var email = decodeTokenEmail(token);
  var isOwner = checkIsOwner(email);

  if (!isOwner) {
    return { success: false, error: 'Insufficient permissions' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();
  var admins = [];

  for (var i = 1; i < allData.length; i++) {
    admins.push({
      admin_id: allData[i][0],
      email: allData[i][1],
      name: allData[i][2],
      role: allData[i][3],
      status: allData[i][4],
      created_at: allData[i][9]
    });
  }

  return {
    success: true,
    data: admins
  };
}

function handleAddAdmin(data) {
  var token = data.token || '';
  var email = data.email || '';
  var name = data.name || '';
  var role = data.role || 'editor';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var requesterEmail = decodeTokenEmail(token);
  if (!checkIsOwner(requesterEmail)) {
    return { success: false, error: 'Insufficient permissions' };
  }

  if (!email || !name) {
    return { success: false, error: 'Missing email or name' };
  }

  if (!isValidEmail(email)) {
    return { success: false, error: 'Invalid email address' };
  }

  // Check if email already exists
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] === email) {
      return { success: false, error: 'Email already exists' };
    }
  }

  // Generate admin ID
  var adminId = 'AD-' + new Date().getTime();

  // Add to sheet
  var now = new Date();
  sheet.appendRow([
    adminId,
    email,
    name,
    role,
    'active',
    '',
    '',
    '',
    '',
    now
  ]);

  // Send invite email
  var subject = 'Welcome to The 2030 Intelligence Report Admin Panel';
  var htmlBody = getAdminInviteEmailTemplate(name, email, role);

  try {
    GmailApp.sendEmail(email, subject, '', {
      htmlBody: htmlBody
    });
  } catch (e) {
    // Log but don't fail
  }

  return {
    success: true,
    admin_id: adminId
  };
}

function handleRemoveAdmin(data) {
  var token = data.token || '';
  var adminId = data.admin_id || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var requesterEmail = decodeTokenEmail(token);
  if (!checkIsOwner(requesterEmail)) {
    return { success: false, error: 'Insufficient permissions' };
  }

  if (!adminId) {
    return { success: false, error: 'Missing admin_id' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][0] === adminId) {
      sheet.getRange(i + 1, 5).setValue('inactive');
      return { success: true };
    }
  }

  return { success: false, error: 'Admin not found' };
}

// ============================================================================
// ADVISOR MANAGEMENT HANDLERS
// ============================================================================

function handleListAdvisors(data) {
  var token = data.token || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADVISORS);
  var allData = sheet.getDataRange().getValues();
  var advisors = [];

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][4] !== 'inactive') {
      advisors.push({
        advisor_id: allData[i][0],
        email: allData[i][1],
        name: allData[i][2],
        expertise: allData[i][3],
        access_level: allData[i][5],
        topics: allData[i][6],
        status: allData[i][4],
        created_at: allData[i][7]
      });
    }
  }

  return {
    success: true,
    data: advisors
  };
}

function handleAddAdvisor(data) {
  var token = data.token || '';
  var email = data.email || '';
  var name = data.name || '';
  var expertise = data.expertise || '';
  var accessLevel = data.access_level || 'viewer';
  var topics = data.topics || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!email || !name) {
    return { success: false, error: 'Missing email or name' };
  }

  if (!isValidEmail(email)) {
    return { success: false, error: 'Invalid email address' };
  }

  // Check if email already exists
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADVISORS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] === email && allData[i][4] !== 'inactive') {
      return { success: false, error: 'Email already exists' };
    }
  }

  // Generate advisor ID
  var advisorId = 'AV-' + new Date().getTime();

  // Add to sheet
  var now = new Date();
  sheet.appendRow([
    advisorId,
    email,
    name,
    expertise,
    'active',
    accessLevel,
    topics,
    now
  ]);

  // Send welcome email
  var subject = 'Welcome to The 2030 Intelligence Report Advisor Program';
  var htmlBody = getAdvisorWelcomeEmailTemplate(name);

  try {
    GmailApp.sendEmail(email, subject, '', {
      htmlBody: htmlBody
    });
  } catch (e) {
    // Log but don't fail
  }

  return {
    success: true,
    advisor_id: advisorId
  };
}

function handleRemoveAdvisor(data) {
  var token = data.token || '';
  var advisorId = data.advisor_id || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!advisorId) {
    return { success: false, error: 'Missing advisor_id' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADVISORS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][0] === advisorId) {
      sheet.getRange(i + 1, 5).setValue('inactive');
      return { success: true };
    }
  }

  return { success: false, error: 'Advisor not found' };
}

// ============================================================================
// ACTION ITEMS HANDLERS
// ============================================================================

function handleListActions(data) {
  var token = data.token || '';
  var statusFilter = data.status_filter || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ACTIONS);
  var allData = sheet.getDataRange().getValues();
  var actions = [];

  for (var i = 1; i < allData.length; i++) {
    var status = allData[i][4];

    if (statusFilter && status !== statusFilter) {
      continue;
    }

    actions.push({
      action_id: allData[i][0],
      title: allData[i][1],
      description: allData[i][2],
      assigned_to: allData[i][3],
      status: status,
      priority: allData[i][5],
      due_date: allData[i][6],
      notes: allData[i][7],
      created_at: allData[i][8],
      updated_at: allData[i][9]
    });
  }

  return {
    success: true,
    data: actions
  };
}

function handleCreateAction(data) {
  var token = data.token || '';
  var title = data.title || '';
  var description = data.description || '';
  var assignedTo = data.assigned_to || '';
  var priority = data.priority || 'normal';
  var dueDate = data.due_date || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!title) {
    return { success: false, error: 'Missing title' };
  }

  var actionId = 'AC-' + new Date().getTime();
  var now = new Date();

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ACTIONS);
  sheet.appendRow([
    actionId,
    title,
    description,
    assignedTo,
    'open',
    priority,
    dueDate,
    '',
    now,
    now
  ]);

  return {
    success: true,
    action_id: actionId
  };
}

function handleUpdateAction(data) {
  var token = data.token || '';
  var actionId = data.action_id || '';
  var status = data.status || '';
  var notes = data.notes || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  if (!actionId) {
    return { success: false, error: 'Missing action_id' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ACTIONS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][0] === actionId) {
      if (status) {
        sheet.getRange(i + 1, 5).setValue(status);
      }
      if (notes) {
        sheet.getRange(i + 1, 8).setValue(notes);
      }
      sheet.getRange(i + 1, 10).setValue(new Date());
      return { success: true };
    }
  }

  return { success: false, error: 'Action not found' };
}

// ============================================================================
// ANALYTICS HANDLERS
// ============================================================================

function handleGetAnalytics(data) {
  var token = data.token || '';
  var dateRange = data.date_range || '7d';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  var allData = sheet.getDataRange().getValues();

  var analytics = [];
  for (var i = 1; i < allData.length; i++) {
    analytics.push({
      date: allData[i][0],
      total_views: allData[i][1],
      unique_visitors: allData[i][2],
      articles_published: allData[i][3],
      feedback_received: allData[i][4],
      avg_session_duration: allData[i][5],
      bounce_rate: allData[i][6]
    });
  }

  return {
    success: true,
    date_range: dateRange,
    data: analytics
  };
}

function handleGetPerformance(data) {
  var token = data.token || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONTENT_PERF);
  var allData = sheet.getDataRange().getValues();

  var performance = [];
  for (var i = 1; i < allData.length; i++) {
    performance.push({
      article_id: allData[i][0],
      title: allData[i][1],
      publish_date: allData[i][2],
      views: allData[i][3],
      engagement_rate: allData[i][4],
      avg_time_on_page: allData[i][5],
      shares: allData[i][6]
    });
  }

  return {
    success: true,
    data: performance
  };
}

// ============================================================================
// DASHBOARD HANDLER
// ============================================================================

function handleGetDashboard(data) {
  var token = data.token || '';

  if (!validateToken(token)) {
    return { success: false, error: 'Invalid token' };
  }

  // Count new feedback
  var feedbackSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var feedbackData = feedbackSheet.getDataRange().getValues();
  var newFeedbackCount = 0;
  var recentFeedback = [];

  for (var i = feedbackData.length - 1; i >= 1 && recentFeedback.length < 5; i--) {
    if (feedbackData[i][11] === 'new') {
      newFeedbackCount++;
    }
    recentFeedback.push({
      feedback_id: feedbackData[i][0],
      user_email: feedbackData[i][1],
      message: feedbackData[i][4],
      type: feedbackData[i][3],
      created_at: feedbackData[i][9]
    });
  }

  // Count actions due today
  var actionSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ACTIONS);
  var actionData = actionSheet.getDataRange().getValues();
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var actionsDueToday = 0;

  for (var i = 1; i < actionData.length; i++) {
    var dueDate = new Date(actionData[i][6]);
    dueDate.setHours(0, 0, 0, 0);
    if (dueDate.getTime() === today.getTime() && actionData[i][4] === 'open') {
      actionsDueToday++;
    }
  }

  // Get analytics summary
  var analyticsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  var analyticsData = analyticsSheet.getDataRange().getValues();
  var totalViews7d = 0;

  for (var i = Math.max(1, analyticsData.length - 7); i < analyticsData.length; i++) {
    totalViews7d += analyticsData[i][1];
  }

  // Get top and bottom articles
  var contentSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONTENT_PERF);
  var contentData = contentSheet.getDataRange().getValues();

  var contentArray = [];
  for (var i = 1; i < contentData.length; i++) {
    contentArray.push({
      title: contentData[i][1],
      views: contentData[i][3],
      engagement_rate: contentData[i][4]
    });
  }

  contentArray.sort(function(a, b) {
    return b.views - a.views;
  });

  var topArticles = contentArray.slice(0, 3);
  var bottomArticles = contentArray.slice(-3).reverse();

  return {
    success: true,
    new_feedback_count: newFeedbackCount,
    actions_due_today: actionsDueToday,
    total_views_7d: totalViews7d,
    top_articles: topArticles,
    bottom_articles: bottomArticles,
    recent_feedback: recentFeedback
  };
}

// ============================================================================
// EMAIL REPORT FUNCTIONS
// ============================================================================

function sendDailyDigest() {
  var configSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONFIG);
  var configData = configSheet.getDataRange().getValues();

  var ownerEmail = '';
  for (var i = 1; i < configData.length; i++) {
    if (configData[i][0] === 'owner_email') {
      ownerEmail = configData[i][1];
      break;
    }
  }

  if (!ownerEmail) {
    return;
  }

  // Get yesterday's data
  var yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  var yesterdayStr = Utilities.formatDate(yesterday, Session.getScriptTimeZone(), 'yyyy-MM-dd');

  var analyticsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  var analyticsData = analyticsSheet.getDataRange().getValues();

  var yesterdayStats = null;
  for (var i = 1; i < analyticsData.length; i++) {
    if (Utilities.formatDate(new Date(analyticsData[i][0]), Session.getScriptTimeZone(), 'yyyy-MM-dd') === yesterdayStr) {
      yesterdayStats = analyticsData[i];
      break;
    }
  }

  // Get new feedback from yesterday
  var feedbackSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_FEEDBACK);
  var feedbackData = feedbackSheet.getDataRange().getValues();
  var newFeedback = [];

  for (var i = 1; i < feedbackData.length; i++) {
    var createdDate = Utilities.formatDate(new Date(feedbackData[i][9]), Session.getScriptTimeZone(), 'yyyy-MM-dd');
    if (createdDate === yesterdayStr && feedbackData[i][5] === 'open') {
      newFeedback.push(feedbackData[i]);
    }
  }

  // Get actions due today
  var actionSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ACTIONS);
  var actionData = actionSheet.getDataRange().getValues();
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var actionsDueToday = [];

  for (var i = 1; i < actionData.length; i++) {
    var dueDate = new Date(actionData[i][6]);
    dueDate.setHours(0, 0, 0, 0);
    if (dueDate.getTime() === today.getTime() && actionData[i][4] === 'open') {
      actionsDueToday.push(actionData[i]);
    }
  }

  var subject = 'Daily Digest - 2030 Intelligence Report - ' + Utilities.formatDate(today, Session.getScriptTimeZone(), 'MMM dd, yyyy');
  var htmlBody = getDailyDigestEmailTemplate(yesterdayStats, newFeedback, actionsDueToday);

  GmailApp.sendEmail(ownerEmail, subject, '', {
    htmlBody: htmlBody
  });
}

function sendWeeklyReport() {
  var configSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONFIG);
  var configData = configSheet.getDataRange().getValues();

  var ownerEmail = '';
  for (var i = 1; i < configData.length; i++) {
    if (configData[i][0] === 'owner_email') {
      ownerEmail = configData[i][1];
      break;
    }
  }

  if (!ownerEmail) {
    return;
  }

  // Get last 7 days of analytics
  var analyticsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  var analyticsData = analyticsSheet.getDataRange().getValues();

  var weeklyStats = [];
  for (var i = Math.max(1, analyticsData.length - 7); i < analyticsData.length; i++) {
    weeklyStats.push({
      date: analyticsData[i][0],
      views: analyticsData[i][1],
      unique_visitors: analyticsData[i][2],
      articles_published: analyticsData[i][3],
      feedback: analyticsData[i][4]
    });
  }

  // Get top content
  var contentSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONTENT_PERF);
  var contentData = contentSheet.getDataRange().getValues();

  var topContent = [];
  for (var i = 1; i < contentData.length; i++) {
    topContent.push({
      title: contentData[i][1],
      views: contentData[i][3],
      engagement: contentData[i][4]
    });
  }

  topContent.sort(function(a, b) {
    return b.views - a.views;
  });

  topContent = topContent.slice(0, 10);

  var admins = getSheetData(SHEET_NAME_ADMINS);
  var adminEmails = [];
  for (var i = 0; i < admins.length; i++) {
    if (admins[i][4] !== 'inactive') {
      adminEmails.push(admins[i][1]);
    }
  }

  var today = new Date();
  var subject = 'Weekly Report - 2030 Intelligence Report - Week of ' + Utilities.formatDate(today, Session.getScriptTimeZone(), 'MMM dd, yyyy');
  var htmlBody = getWeeklyReportEmailTemplate(weeklyStats, topContent);

  for (var i = 0; i < adminEmails.length; i++) {
    GmailApp.sendEmail(adminEmails[i], subject, '', {
      htmlBody: htmlBody
    });
  }
}

function sendMonthlyReport() {
  var configSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_CONFIG);
  var configData = configSheet.getDataRange().getValues();

  var ownerEmail = '';
  for (var i = 1; i < configData.length; i++) {
    if (configData[i][0] === 'owner_email') {
      ownerEmail = configData[i][1];
      break;
    }
  }

  if (!ownerEmail) {
    return;
  }

  // Get last 30 days of analytics
  var analyticsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  var analyticsData = analyticsSheet.getDataRange().getValues();

  var totalViews = 0;
  var totalArticles = 0;
  var totalFeedback = 0;
  var avgEngagement = 0;

  for (var i = Math.max(1, analyticsData.length - 30); i < analyticsData.length; i++) {
    totalViews += analyticsData[i][1];
    totalArticles += analyticsData[i][3];
    totalFeedback += analyticsData[i][4];
  }

  var dataPointsCount = Math.min(analyticsData.length - 1, 30);
  if (dataPointsCount > 0) {
    avgEngagement = totalFeedback / totalViews;
  }

  var today = new Date();
  var subject = 'Monthly Executive Summary - 2030 Intelligence Report - ' + Utilities.formatDate(today, Session.getScriptTimeZone(), 'MMMM yyyy');
  var htmlBody = getMonthlyReportEmailTemplate(totalViews, totalArticles, totalFeedback, avgEngagement);

  GmailApp.sendEmail(ownerEmail, subject, '', {
    htmlBody: htmlBody
  });
}

function setupTriggers() {
  // Remove existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendDailyDigest' ||
        triggers[i].getHandlerFunction() === 'sendWeeklyReport' ||
        triggers[i].getHandlerFunction() === 'sendMonthlyReport') {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  // Create new triggers
  // Daily at 9 AM
  ScriptApp.newTrigger('sendDailyDigest')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .create();

  // Weekly on Monday at 9 AM
  ScriptApp.newTrigger('sendWeeklyReport')
    .timeBased()
    .atHour(9)
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .create();

  // Monthly on 1st at 9 AM
  ScriptApp.newTrigger('sendMonthlyReport')
    .timeBased()
    .atHour(9)
    .onMonthDay(1)
    .create();
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function initializeSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

  // Create sheets if they don't exist
  var sheetNames = [
    SHEET_NAME_CONFIG,
    SHEET_NAME_ADMINS,
    SHEET_NAME_ADVISORS,
    SHEET_NAME_FEEDBACK,
    SHEET_NAME_ACTIONS,
    SHEET_NAME_ANALYTICS_DAILY,
    SHEET_NAME_CONTENT_PERF,
    SHEET_NAME_EMAIL_REPORTS
  ];

  for (var i = 0; i < sheetNames.length; i++) {
    var sheetName = sheetNames[i];
    if (!spreadsheet.getSheetByName(sheetName)) {
      spreadsheet.insertSheet(sheetName);
    }
  }

  // Initialize Config sheet
  var configSheet = spreadsheet.getSheetByName(SHEET_NAME_CONFIG);
  if (configSheet.getLastRow() === 0) {
    configSheet.appendRow(['key', 'value']);
    configSheet.appendRow(['owner_email', 'narenbizymoms@gmail.com']);
  }

  // Initialize Admins sheet
  var adminsSheet = spreadsheet.getSheetByName(SHEET_NAME_ADMINS);
  if (adminsSheet.getLastRow() === 0) {
    adminsSheet.appendRow(['admin_id', 'email', 'name', 'role', 'status', 'otp', 'otp_expiry', 'last_login', 'last_activity', 'created_at']);
    adminsSheet.appendRow(['AD-0001', 'narenbizymoms@gmail.com', 'Admin Owner', 'owner', 'active', '', '', '', '', new Date()]);
  }

  // Initialize Advisors sheet
  var advisorsSheet = spreadsheet.getSheetByName(SHEET_NAME_ADVISORS);
  if (advisorsSheet.getLastRow() === 0) {
    advisorsSheet.appendRow(['advisor_id', 'email', 'name', 'expertise', 'status', 'access_level', 'topics', 'created_at']);
  }

  // Initialize Feedback sheet
  var feedbackSheet = spreadsheet.getSheetByName(SHEET_NAME_FEEDBACK);
  if (feedbackSheet.getLastRow() === 0) {
    feedbackSheet.appendRow(['feedback_id', 'user_email', 'page_url', 'feedback_type', 'message', 'status', 'priority', 'assigned_to', 'reply', 'created_at', 'updated_at', 'flag']);
  }

  // Initialize ActionItems sheet
  var actionSheet = spreadsheet.getSheetByName(SHEET_NAME_ACTIONS);
  if (actionSheet.getLastRow() === 0) {
    actionSheet.appendRow(['action_id', 'title', 'description', 'assigned_to', 'status', 'priority', 'due_date', 'notes', 'created_at', 'updated_at']);
  }

  // Initialize Analytics_Daily sheet
  var analyticsSheet = spreadsheet.getSheetByName(SHEET_NAME_ANALYTICS_DAILY);
  if (analyticsSheet.getLastRow() === 0) {
    analyticsSheet.appendRow(['date', 'total_views', 'unique_visitors', 'articles_published', 'feedback_received', 'avg_session_duration', 'bounce_rate']);
  }

  // Initialize ContentPerformance sheet
  var contentSheet = spreadsheet.getSheetByName(SHEET_NAME_CONTENT_PERF);
  if (contentSheet.getLastRow() === 0) {
    contentSheet.appendRow(['article_id', 'title', 'publish_date', 'views', 'engagement_rate', 'avg_time_on_page', 'shares']);
  }

  // Initialize EmailReports sheet
  var emailSheet = spreadsheet.getSheetByName(SHEET_NAME_EMAIL_REPORTS);
  if (emailSheet.getLastRow() === 0) {
    emailSheet.appendRow(['report_type', 'sent_at', 'recipient', 'status']);
  }

  // Store JWT_SECRET in script properties if not exists
  var scriptProperties = PropertiesService.getScriptProperties();
  if (!scriptProperties.getProperty(JWT_SECRET)) {
    scriptProperties.setProperty(JWT_SECRET, Utilities.getUuid());
  }
}

function getSheetData(sheetName) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  return sheet.getDataRange().getValues();
}

function generateToken(email) {
  var scriptProperties = PropertiesService.getScriptProperties();
  var secret = scriptProperties.getProperty(JWT_SECRET);

  var now = new Date();
  var timestamp = now.getTime().toString();
  var message = email + '|' + timestamp;

  var signature = hmacSha256(message, secret);
  var token = Utilities.base64Encode(message + '|' + signature);

  return token;
}

function validateToken(token) {
  if (!token) {
    return false;
  }

  try {
    var decoded = Utilities.base64Decode(token);
    var decodedStr = '';
    for (var i = 0; i < decoded.length; i++) {
      decodedStr += String.fromCharCode(decoded[i]);
    }

    var parts = decodedStr.split('|');
    if (parts.length !== 3) {
      return false;
    }

    var email = parts[0];
    var timestamp = parts[1];
    var signature = parts[2];

    var scriptProperties = PropertiesService.getScriptProperties();
    var secret = scriptProperties.getProperty(JWT_SECRET);

    var message = email + '|' + timestamp;
    var expectedSignature = hmacSha256(message, secret);

    if (signature !== expectedSignature) {
      return false;
    }

    // Check expiry (8 hours)
    var now = new Date().getTime();
    var tokenTime = parseInt(timestamp);
    var expiryTime = 8 * 60 * 60 * 1000; // 8 hours in milliseconds

    if (now - tokenTime > expiryTime) {
      return false;
    }

    return true;
  } catch (e) {
    return false;
  }
}

function decodeTokenEmail(token) {
  try {
    var decoded = Utilities.base64Decode(token);
    var decodedStr = '';
    for (var i = 0; i < decoded.length; i++) {
      decodedStr += String.fromCharCode(decoded[i]);
    }

    var parts = decodedStr.split('|');
    if (parts.length === 3) {
      return parts[0];
    }
  } catch (e) {
    // Silently fail
  }

  return '';
}

function hmacSha256(message, secret) {
  var signature = Utilities.computeHmacSha256Signature(message, secret);
  var signatureStr = '';
  for (var i = 0; i < signature.length; i++) {
    var byte = (signature[i] < 0) ? signature[i] + 256 : signature[i];
    signatureStr += ('0' + byte.toString(16)).slice(-2);
  }
  return signatureStr;
}

function isValidEmail(email) {
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function checkIsOwner(email) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME_ADMINS);
  var allData = sheet.getDataRange().getValues();

  for (var i = 1; i < allData.length; i++) {
    if (allData[i][1] === email && allData[i][3] === 'owner') {
      return true;
    }
  }

  return false;
}

function buildJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================================================================
// EMAIL TEMPLATES
// ============================================================================

function getOtpEmailTemplate(otp, email) {
  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">2030 Intelligence Report</h1>' +
    '<h2>Your Login Code</h2>' +
    '<p>Hello ' + email + ',</p>' +
    '<p>Your one-time login code is:</p>' +
    '<div style="background: #f5f5f5; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">' +
    '<h1 style="letter-spacing: 5px; color: #2980b9; font-family: monospace;">' + otp + '</h1>' +
    '</div>' +
    '<p>This code expires in 15 minutes.</p>' +
    '<p>If you did not request this code, you can safely ignore this email.</p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report Admin Panel</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getFeedbackReplyEmailTemplate(reply) {
  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">2030 Intelligence Report</h1>' +
    '<h2>Your Feedback Has Been Reviewed</h2>' +
    '<p>Thank you for your valuable feedback!</p>' +
    '<div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">' +
    '<p>' + reply + '</p>' +
    '</div>' +
    '<p>We appreciate your input and will continue to improve our content.</p>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com" style="color: #2980b9;">Return to The 2030 Intelligence Report</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getAdminInviteEmailTemplate(name, email, role) {
  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">2030 Intelligence Report</h1>' +
    '<h2>Welcome to the Admin Panel, ' + name + '!</h2>' +
    '<p>You have been added as an <strong>' + role + '</strong> to the 2030 Intelligence Report Admin Panel.</p>' +
    '<p>To get started, visit the admin panel and request a login code.</p>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com/admin" style="background: #2980b9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Access Admin Panel</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report Admin Panel</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getAdvisorWelcomeEmailTemplate(name) {
  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">2030 Intelligence Report</h1>' +
    '<h2>Welcome to the Advisor Program, ' + name + '!</h2>' +
    '<p>We are excited to have you join the 2030 Intelligence Report as an advisor.</p>' +
    '<p>As an advisor, you will have access to exclusive content and opportunities to contribute to our platform.</p>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com/advisor" style="background: #2980b9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Access Your Profile</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getDailyDigestEmailTemplate(yesterdayStats, newFeedback, actionsDueToday) {
  var feedbackHtml = '';
  for (var i = 0; i < newFeedback.length; i++) {
    feedbackHtml += '<tr><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      newFeedback[i][1] + ' - ' + newFeedback[i][4].substring(0, 100) + '...</td></tr>';
  }

  var actionsHtml = '';
  for (var i = 0; i < actionsDueToday.length; i++) {
    actionsHtml += '<tr><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      actionsDueToday[i][1] + ' - Assigned to: ' + actionsDueToday[i][3] + '</td></tr>';
  }

  var viewsCount = yesterdayStats ? yesterdayStats[1] : 0;
  var articlesCount = yesterdayStats ? yesterdayStats[3] : 0;

  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">Daily Digest</h1>' +
    '<h2>Yesterday\'s Summary</h2>' +
    '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">' +
    '<div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">' +
    '<h3 style="margin: 0 0 10px 0; color: #2980b9;">Total Views</h3>' +
    '<p style="margin: 0; font-size: 24px; font-weight: bold;">' + viewsCount + '</p>' +
    '</div>' +
    '<div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">' +
    '<h3 style="margin: 0 0 10px 0; color: #27ae60;">Articles Published</h3>' +
    '<p style="margin: 0; font-size: 24px; font-weight: bold;">' + articlesCount + '</p>' +
    '</div>' +
    '</div>' +
    '<h2>New Feedback</h2>' +
    '<table style="width: 100%; border-collapse: collapse;">' +
    feedbackHtml +
    '</table>' +
    '<h2>Actions Due Today</h2>' +
    '<table style="width: 100%; border-collapse: collapse;">' +
    actionsHtml +
    '</table>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com/admin" style="background: #2980b9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Full Dashboard</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report Daily Digest</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getWeeklyReportEmailTemplate(weeklyStats, topContent) {
  var statsHtml = '';
  var totalViews = 0;
  for (var i = 0; i < weeklyStats.length; i++) {
    totalViews += weeklyStats[i].views;
    statsHtml += '<tr><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      weeklyStats[i].date + '</td><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      weeklyStats[i].views + ' views</td></tr>';
  }

  var contentHtml = '';
  for (var i = 0; i < topContent.length; i++) {
    contentHtml += '<tr><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      (i + 1) + '. ' + topContent[i].title + '</td><td style="padding: 10px; border-bottom: 1px solid #eee;">' +
      contentHtml[i].views + ' views</td></tr>';
  }

  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">Weekly Report</h1>' +
    '<h2>This Week in Numbers</h2>' +
    '<div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">' +
    '<h3 style="margin: 0 0 10px 0;">Total Views: <span style="color: #2980b9;">' + totalViews + '</span></h3>' +
    '</div>' +
    '<h2>Daily Breakdown</h2>' +
    '<table style="width: 100%; border-collapse: collapse;">' +
    '<tr><th style="text-align: left; padding: 10px; background: #f5f5f5;">Date</th><th style="text-align: left; padding: 10px; background: #f5f5f5;">Views</th></tr>' +
    statsHtml +
    '</table>' +
    '<h2>Top Content</h2>' +
    '<table style="width: 100%; border-collapse: collapse;">' +
    '<tr><th style="text-align: left; padding: 10px; background: #f5f5f5;">Article</th><th style="text-align: left; padding: 10px; background: #f5f5f5;">Views</th></tr>' +
    contentHtml +
    '</table>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com/admin" style="background: #2980b9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Full Analytics</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report Weekly Report</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}

function getMonthlyReportEmailTemplate(totalViews, totalArticles, totalFeedback, avgEngagement) {
  var engagementPercent = (avgEngagement * 100).toFixed(2);

  return '<html>' +
    '<head><style>body { font-family: Arial, sans-serif; color: #333; }</style></head>' +
    '<body>' +
    '<div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">' +
    '<h1 style="color: #2c3e50;">Monthly Executive Summary</h1>' +
    '<h2>30-Day Performance Overview</h2>' +
    '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">' +
    '<div style="background: #e8f4f8; padding: 20px; border-radius: 5px; text-align: center;">' +
    '<h3 style="margin: 0 0 10px 0; color: #2980b9;">Total Views</h3>' +
    '<p style="margin: 0; font-size: 32px; font-weight: bold; color: #2980b9;">' + totalViews + '</p>' +
    '</div>' +
    '<div style="background: #e8f8e8; padding: 20px; border-radius: 5px; text-align: center;">' +
    '<h3 style="margin: 0 0 10px 0; color: #27ae60;">Articles Published</h3>' +
    '<p style="margin: 0; font-size: 32px; font-weight: bold; color: #27ae60;">' + totalArticles + '</p>' +
    '</div>' +
    '<div style="background: #f8e8e8; padding: 20px; border-radius: 5px; text-align: center;">' +
    '<h3 style="margin: 0 0 10px 0; color: #e74c3c;">Feedback Received</h3>' +
    '<p style="margin: 0; font-size: 32px; font-weight: bold; color: #e74c3c;">' + totalFeedback + '</p>' +
    '</div>' +
    '<div style="background: #f8f8e8; padding: 20px; border-radius: 5px; text-align: center;">' +
    '<h3 style="margin: 0 0 10px 0; color: #f39c12;">Engagement Rate</h3>' +
    '<p style="margin: 0; font-size: 32px; font-weight: bold; color: #f39c12;">' + engagementPercent + '%</p>' +
    '</div>' +
    '</div>' +
    '<h2>Key Insights</h2>' +
    '<ul>' +
    '<li>Total platform views reached ' + totalViews + ' this month</li>' +
    '<li>Published ' + totalArticles + ' new articles to drive engagement</li>' +
    '<li>Received ' + totalFeedback + ' feedback submissions from users</li>' +
    '<li>Engagement rate maintained at ' + engagementPercent + '%</li>' +
    '</ul>' +
    '<p style="margin-top: 30px;"><a href="https://ai2030report.com/admin" style="background: #2980b9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Detailed Analytics</a></p>' +
    '<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">' +
    '<p style="font-size: 12px; color: #999;">2030 Intelligence Report Executive Summary</p>' +
    '</div>' +
    '</body>' +
    '</html>';
}
