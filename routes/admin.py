"""
Admin routes for cache management and system monitoring
"""
from flask import Blueprint, render_template, jsonify, flash, redirect, url_for
from services.cache_service import CacheService
import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)

@admin_bp.route('/admin/cache/stats')
def cache_stats():
    """Get cache statistics (for debugging/monitoring)"""
    try:
        cache_service = CacheService()
        stats = cache_service.get_cache_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/cache/clear', methods=['POST'])
def clear_cache():
    """Clear cache (for debugging/maintenance)"""
    try:
        cache_service = CacheService()
        cache_service.clear_cache()
        return jsonify({'success': True, 'message': 'Cache cleared successfully'})
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({'error': str(e)}), 500