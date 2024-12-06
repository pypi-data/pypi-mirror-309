interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// 统一的错误处理
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`API 错误: ${response.status} ${response.statusText}`);
  }
  const data = await response.json();
  return data;
}

// 获取配置
export async function fetchConfig(): Promise<ApiResponse<any>> {
  try {
    const response = await fetch('/api/config');
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('获取配置失败:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : '获取配置失败'
    };
  }
}

// 更新配置
export async function updateConfig(config: any): Promise<ApiResponse<any>> {
  try {
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('更新配置失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '更新配置失败'
    };
  }
}

// 获取历史记录
export async function fetchHistory(): Promise<ApiResponse<any>> {
  try {
    const response = await fetch('/api/history');
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('获取历史记录失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '获取历史记录失败'
    };
  }
}

// 删除历史记录
export async function deleteHistoryItem(id: string): Promise<ApiResponse<any>> {
  try {
    const response = await fetch(`/api/history/${id}`, {
      method: 'DELETE',
    });
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('删除历史记录失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '删除历史记录失败'
    };
  }
}

// 更新排除模式
export async function updateExcludePatterns(patterns: {
  directories: string[];
  files: string[];
}): Promise<ApiResponse<any>> {
  try {
    const response = await fetch('/api/exclude', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(patterns),
    });
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('更新排除模式失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '更新排除模式失败'
    };
  }
}

// 获取首页数据
export async function fetchHomeData(): Promise<ApiResponse<any>> {
  try {
    const response = await fetch('/api');
    const data = await handleResponse(response);
    return { success: true, data };
  } catch (error) {
    console.error('获取首页数据失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '获取首页数据失败'
    };
  }
} 